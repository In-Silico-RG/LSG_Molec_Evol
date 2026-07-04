#!/usr/bin/env python3
"""
Sequential (uncontended) re-run of Experiment 2's 3x3 factorial grid.
Mirrors the execution protocol of 03-Evolutionary_Experiment.ipynb
(Experiment 1: one LGS process at a time, no ThreadPoolExecutor),
applied to Experiment 2's 9 configurations, to obtain t_gen
measurements that are directly comparable to Experiment 1's.
"""

import os
import sys
import glob
import shutil
import subprocess
import time
import csv
import random
from datetime import datetime

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
JAR_PATH = os.path.join(BASE_PATH, "lgs_gen.jar")
RESOURCES_DIR = os.path.join(BASE_PATH, "resources")
OUTPUT_DIR = os.path.join(BASE_PATH, "output")
RESULTS_CSV = os.path.join(BASE_PATH, "exp2_sequential_results.csv")
N_REPLICAS = int(sys.argv[1]) if len(sys.argv) > 1 else 30

assert os.path.exists(JAR_PATH), f"lgs_gen.jar not found at {JAR_PATH}"

CONFIG_META = {
    "SW_fBO4_sg0":   {"group": "SW", "fBO4": 0.54, "sg_ratio": 0.0},
    "SW_fBO4_sg08":  {"group": "SW", "fBO4": 0.54, "sg_ratio": 0.8},
    "SW_fBO4_sg15":  {"group": "SW", "fBO4": 0.54, "sg_ratio": 1.5},
    "HW_fBO4_sg0":   {"group": "HW", "fBO4": 0.69, "sg_ratio": 0.0},
    "HW_fBO4_sg08":  {"group": "HW", "fBO4": 0.69, "sg_ratio": 0.8},
    "HW_fBO4_sg15":  {"group": "HW", "fBO4": 0.69, "sg_ratio": 1.5},
    "GR_fBO4_sg0":   {"group": "GR", "fBO4": 0.77, "sg_ratio": 0.0},
    "GR_fBO4_sg08":  {"group": "GR", "fBO4": 0.77, "sg_ratio": 0.8},
    "GR_fBO4_sg15":  {"group": "GR", "fBO4": 0.77, "sg_ratio": 1.5},
}

EXPERIMENT_CONFIGS = sorted(glob.glob(os.path.join(RESOURCES_DIR, "*_config.yaml")))
assert len(EXPERIMENT_CONFIGS) == 9, f"expected 9 configs, found {len(EXPERIMENT_CONFIGS)}"

CSV_FIELDS = ["config", "group", "fBO4", "sg_ratio", "dp", "replica",
              "t_gen", "success", "error", "timestamp"]


def run_lgs_once(config_file, timeout=900):
    config_name = os.path.basename(config_file).replace("_config.yaml", "")
    project_config = os.path.join(RESOURCES_DIR, "project_config.yaml")

    backup = None
    if os.path.exists(project_config):
        backup = project_config + ".backup"
        shutil.move(project_config, backup)

    t_gen, success, error_msg = None, False, ""
    try:
        shutil.copy2(config_file, project_config)
        t_start = time.time()
        result = subprocess.run(
            ["java", "-jar", JAR_PATH],
            cwd=BASE_PATH,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        t_gen = time.time() - t_start
        success = (result.returncode == 0)
        if not success:
            error_msg = (result.stderr or "")[-500:]
    except subprocess.TimeoutExpired:
        t_gen = timeout
        error_msg = f"timeout after {timeout}s"
    except Exception as e:
        error_msg = str(e)
    finally:
        if os.path.exists(project_config):
            os.remove(project_config)
        if backup:
            shutil.move(backup, project_config)
        for sub in ("json", "matrices", "mol", "png", "sdf", "struct"):
            for p in glob.glob(os.path.join(OUTPUT_DIR, "**", sub), recursive=True):
                shutil.rmtree(p, ignore_errors=True)
        shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    return config_name, t_gen, success, error_msg


def main():
    tasks = []
    for config_file in EXPERIMENT_CONFIGS:
        for rep in range(1, N_REPLICAS + 1):
            tasks.append((config_file, rep))
    random.shuffle(tasks)

    write_header = not os.path.exists(RESULTS_CSV)
    with open(RESULTS_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if write_header:
            writer.writeheader()
        f.flush()

        n_done, n_total = 0, len(tasks)
        t_run_start = time.time()
        for config_file, rep in tasks:
            config_name, t_gen, success, error_msg = run_lgs_once(config_file)
            meta = CONFIG_META[config_name]
            row = {
                "config": config_name,
                "group": meta["group"],
                "fBO4": meta["fBO4"],
                "sg_ratio": meta["sg_ratio"],
                "dp": 10,
                "replica": rep,
                "t_gen": round(t_gen, 4) if t_gen is not None else "",
                "success": success,
                "error": error_msg,
                "timestamp": datetime.now().isoformat(),
            }
            writer.writerow(row)
            f.flush()
            n_done += 1
            elapsed = time.time() - t_run_start
            print(f"[{n_done}/{n_total}] {config_name} rep={rep} "
                  f"t_gen={t_gen:.2f}s success={success} "
                  f"elapsed={elapsed/60:.1f}min", flush=True)

    print("DONE")


if __name__ == "__main__":
    main()

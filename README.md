# Non-Monotonic Computational Complexity in Lignin assembly Reveals a Hardwood Transition Peak Across400 Million Years of Plant Evolution

[![License: LGPL v2.1](https://img.shields.io/badge/License-LGPL_v2.1-blue.svg)](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

**IN SILICO Research Group** — Universidad de Sucre, Sincelejo, Colombia  
Minciencias Category C

---

## Overview

This repository contains the data, configuration files, and analysis
notebooks for the paper:

> **Non-Monotonic Computational Complexity in Lignin Assembly Reveals a Hardwood Transition Peak Across
400 Million Years of Plant Evolution**  
> Combariza et al. — *ChemRxiv preprint, 2026*

The central question: does the time required to computationally generate
a lignin structure ($t_{\text{gen}}$) reflect the biosynthetic accessibility
that natural selection has optimized over 400 million years of plant evolution?

---

## Repository Structure

```
├── configs/
│   ├── experiment1/        # 9 YAML configs — Experiment 1 (SW/HW/GR × DP5/8/10)
│   │   └── README_experiment.md   # Experiment 1 design notes
│   └── experiment2/        # 9 YAML configs — Experiment 2 (fBO4 × S/G orthogonal)
├── notebooks/
│   ├── 03-Run_Evolutionary_Experiment.ipynb   # Sequential runner — Experiment 1
│   └── 05-Parallel_Experiment.ipynb           # Parallel runner (8 workers) — Experiment 2
├── results/
│   ├── evolutionary_experiment_results.csv   # Raw data — Experiment 1 (270 rows)
│   └── exp2_parallel_results.csv             # Raw data — Experiment 2 (244 rows, 239 successful)
├── sequential_rerun/
│   ├── run_sequential.py                     # Uncontended sequential re-run of Experiment 2
│   ├── exp2_sequential_results.csv           # Raw data — sequential validation (270 rows, 269 successful)
│   └── resources/                            # 9 YAML configs used by the re-run
├── figures/
│   ├── exp1_barplot.pdf/.png    # Figure 1 — Experiment 1 results
│   └── exp2_heatmap.pdf/.png    # Figure 2 — Experiment 2 heatmap
└── paper/
    ├── Comp_Gen_Time_Evol_Proxy.pdf      # Full manuscript
    └── Comp_Gen_Time_Evol_Proxy_SI.pdf   # Supporting Information
```

All notebooks/scripts run against `lgs_gen.jar`
(Eswaran *et al.*, 2022) placed at the repository root.

The `sequential_rerun/` directory validates that the non-monotonic
hardwood peak found in Experiment 2 is not an artifact of that
experiment's parallel execution regime — an uncontended, one-process-
at-a-time re-run of the same 3×3 factorial grid reproduces the effect
(see SI Section S5.3).

---

## Experimental Design

### Experiment 1 — Phylogenetic Gradient
Tests whether $t_{\text{gen}}$ tracks the established SW → HW → GR
evolutionary gradient at three DP levels.

| Group | fBO4 | S/G | DP levels | n per cell |
|-------|------|-----|-----------|------------|
| SW (Softwood) | 0.54 | 0.0 | 5, 8, 10 | 30 |
| HW (Hardwood) | 0.69 | 1.5 | 5, 8, 10 | 30 |
| GR (Grass)    | 0.77 | 0.8 | 5, 8, 10 | 30 |

**Key result:** Gradient fulfilled at DP=8 only.
Strong plant type × DP interaction (η²=0.970).

### Experiment 2 — Orthogonal Decoupling of fBO4 × S/G
3×3 factorial design at DP=10, varying fBO4 and S/G independently.

**Key result:** fBO4 is the dominant factor (η²=0.712) but its effect
is **non-monotonic** — the intermediate HW level (fBO4=0.69) produces
the longest generation times (mean 282.8s, d=2.28 vs SW, pooled over
S/G). Restricting the comparison to the natural plant-type
configurations (SW/SW=100.8s, HW/HW=288.9s, GR/GR=152.3s), GR/GR is
significantly slower than SW/SW (Δ=51.5s, d=1.47, t(50)=5.28,
p=2.8×10⁻⁶): the grass configuration does not fully revert to the
ancestral complexity level, resolving most but not all of the
complexity introduced at the hardwood transition. The independent
sequential re-run of the same grid (`sequential_rerun/`) confirms
this (d=2.46, p=1.8×10⁻¹³).

---

## Requirements

- Python ≥ 3.10
- Java (OpenJDK ≥ 11) — for LGS (`lgs_gen.jar`)
- `lgs_gen.jar` — Lignin Structure Generator
  ([Eswaran et al., Scientific Data 2022](https://doi.org/10.1038/s41597-022-01709-4))

```bash
pip install pyyaml pandas scipy pingouin matplotlib numpy
```

---

## Running the Experiments

1. Place `lgs_gen.jar` in your working directory.
2. Experiment 1: open `notebooks/03-Run_Evolutionary_Experiment.ipynb`,
   set `BASE_PATH` to your working directory, and run all cells in order.
3. Experiment 2 (parallel): open `notebooks/05-Parallel_Experiment.ipynb`,
   set `BASE_PATH`, set `EXPERIMENT_MODE = 'EXP2'`, and run all cells in order.
4. Experiment 2 (sequential validation): run `sequential_rerun/run_sequential.py`
   directly against the configs in `sequential_rerun/resources/`.

The notebooks generate the YAML configs automatically — no external
files needed beyond `lgs_gen.jar`.

---

## Parameter Grounding

All bondconfig parameters are derived from milled wood lignin (MWL)
literature, not from technical (pulped) lignin:

| Parameter | Source |
|-----------|--------|
| β-O-4 fractions | Eswaran et al. 2022; Obrzut et al. 2023 |
| Linkage distributions | Lourenço & Pereira 2018; Chakar & Ragauskas 2004 |
| S/G ratios | Literature consensus for native MWL |

---

## Citation

```bibtex
@article{combariza2026lignin,
  author  = {Combariza, Aldo F. and others},
  title   = {Non-Monotonic Computational Complexity in Lignin Assembly Reveals a Hardwood Transition Peak Across 400 Million Years of Plant Evolution},
  journal = {ChemRxiv},
  year    = {2026},
  doi     = {TBD}
}
```

---

## License

LGPL-2.1 — see [LICENSE](LICENSE)

## Contact

IN SILICO Research Group  
Universidad de Sucre — Sincelejo, Colombia  
[insilico@unisucre.edu.co](mailto:insilico@unisucre.edu.co)

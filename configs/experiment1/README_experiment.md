# Experimento: Gradiente Evolutivo SW → HW → Grass en t_gen
## Diseño experimental controlado — v1.0

### Hipótesis a probar
Si el gradiente evolutivo SW → HW → Grass se refleja en t_gen, entonces:
  t_gen(SW) > t_gen(HW) > t_gen(GR)
para DP equivalente, con diferencias estadísticamente significativas.

### Variables

| Variable | Tipo | Valores | Fuente |
|---|---|---|---|
| Tipo botánico (SW/HW/GR) | Independiente principal | 3 niveles | Literatura |
| DP | Control (bloqueada) | 5, 8, 10 | Constante por grupo |
| fBO4 | Derivada del tipo botánico | 0.54 / 0.69 / 0.77 | Literatura MWL |
| S/G ratio | Derivada del tipo botánico | 0.0 / 1.5 / 0.8 | Literatura |
| t_gen | Dependiente | continua (segundos) | LGS output |

### Parámetros de bondconfig por grupo (normalizados a 100)

| Grupo | BO4 | B5 | BB | _4O5 | _55 | DBDO | S/G | fBO4 |
|---|---|---|---|---|---|---|---|---|
| SW | 54 | 11 | 3 | 7 | 25 | 0 | 0.0 | 0.540 |
| HW | 69 | 7  | 7 | 7 | 10 | 0 | 1.5 | 0.690 |
| GR | 77 | 5  | 4 | 8 | 6  | 0 | 0.8 | 0.770 |

### Fuentes de la literatura para los valores de bondconfig

- β-O-4 (BO4): SW 43-50%, HW 50-65%, Grass 65-80%
  → Eswaran et al., Sci. Data 2022; RSC Sustainability 2023; ResearchGate tabla comparativa
- β-5 (B5): SW 9-12%, HW 4-8%, Grass 3-7%
  → Literature consensus (S units cannot form β-5, explains HW/GR decrease)
- β-β (BB): SW 2-4%, HW 3-8%, Grass 3-6%
- 4-O-5: SW 4-8%, HW 5-8%, Grass 5-10%
- 5-5 (_55): SW 18-25%, HW 5-12%, Grass 3-8%
  → Higher in SW because G units have free C-5 position for C-C coupling

### Estructura del experimento

3 grupos × 3 niveles de DP × n réplicas = 9 configuraciones
Réplicas recomendadas: n ≥ 30 por configuración

### Análisis estadístico

1. ANOVA de dos factores: tipo_botánico × DP sobre t_gen
2. Test de contraste ortogonal: SW > HW > GR (hipótesis ordenada)
3. Si ANOVA significativo: test post-hoc Tukey HSD
4. Reportar: media ± SD de t_gen por celda, tamaño de efecto (η²)

### Archivos incluidos

- SW_DP5_config.yaml   → Softwood, DP=5
- SW_DP8_config.yaml   → Softwood, DP=8
- SW_DP10_config.yaml  → Softwood, DP=10
- HW_DP5_config.yaml   → Hardwood, DP=5
- HW_DP8_config.yaml   → Hardwood, DP=8
- HW_DP10_config.yaml  → Hardwood, DP=10
- GR_DP5_config.yaml   → Grass, DP=5
- GR_DP8_config.yaml   → Grass, DP=8
- GR_DP10_config.yaml  → Grass, DP=10

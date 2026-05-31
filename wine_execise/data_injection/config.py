import numpy as np

RANDOM_SEED = 42

TARGET_COL = "class"

NUMERIC_COLS = [
    "alcohol", "malic_acid", "ash", "alcalinity_of_ash",
    "magnesium", "total_phenols", "flavanoids", "nonflavanoid_phenols",
    "proanthocyanins", "color_intensity", "hue", "od280_od315", "proline",
]

CORRUPTION_PRESETS = {
    "missing_light": {"type": "missing", "ratio": 0.05, "columns": [TARGET_COL]},
    "missing_heavy": {"type": "missing", "ratio": 0.20, "columns": [TARGET_COL]},
    "noise_low": {"type": "noise", "noise_level": 0.05, "columns": NUMERIC_COLS[:2]},
    "noise_high": {"type": "noise", "noise_level": 0.15, "columns": NUMERIC_COLS[:2]},
    "outliers": {"type": "outliers", "spike_factor": 3.0, "days": 5, "target_cols": NUMERIC_COLS[:5] + [TARGET_COL]},
    "bias": {"type": "bias", "bias_factor": 0.7, "columns": NUMERIC_COLS[:2]},
    "schema_drift": {"type": "schema_drift", "old_col": TARGET_COL, "new_col": "cultivar"},
    "duplicates_light": {"type": "duplicates", "ratio": 0.05},
    "duplicates_heavy": {"type": "duplicates", "ratio": 0.25},
}

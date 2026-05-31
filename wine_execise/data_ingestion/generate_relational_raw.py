import pandas as pd
import numpy as np
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
RELATIONAL_DIR = RAW_DIR / "relational"

RANDOM_SEED = 42

attribute_names = [
    "class", "alcohol", "malic_acid", "ash", "alcalinity_of_ash",
    "magnesium", "total_phenols", "flavanoids", "nonflavanoid_phenols",
    "proanthocyanins", "color_intensity", "hue", "od280_od315", "proline"
]
chemical_cols = ["alcohol", "malic_acid", "ash", "alcalinity_of_ash", "magnesium", "color_intensity", "proline"]
phenol_cols = ["total_phenols", "flavanoids", "nonflavanoid_phenols", "proanthocyanins", "hue", "od280_od315"]


def load_and_clean():
    df = pd.read_csv(RAW_DIR / "wine.data", header=None, names=attribute_names)
    df["class"] = df["class"] - 1
    return df


def generate_relational_data():
    RELATIONAL_DIR.mkdir(parents=True, exist_ok=True)

    df = load_and_clean()
    n = len(df)

    rng = np.random.default_rng(RANDOM_SEED)
    df["sample_id"] = range(1, n + 1)

    # ---- Table 1: cultivar (target, all 178 rows) ----
    cultivar = df[["sample_id", "class"]].copy()
    cultivar.to_csv(RELATIONAL_DIR / "cultivar.csv", index=False)
    print(f"cultivar: {len(cultivar)} rows")

    # ---- Table 2: chemical (chemical measurements) ----
    chemical = df[["sample_id"] + chemical_cols].copy()
    drop_chemical_idx = rng.choice(chemical.index, size=5, replace=False)
    chemical = chemical.drop(drop_chemical_idx)
    chemical = chemical.rename(columns={"sample_id": "chemical_id"})

    fake_chemical_ids = range(n + 1, n + 4)
    real_chemical = chemical[chemical_cols]
    sample_rows = real_chemical.sample(n=3, replace=True, random_state=rng)
    noise = rng.normal(1, 0.03, size=sample_rows.shape)
    perturbed = np.clip(sample_rows * noise, 0, None)

    fake_chemical = pd.DataFrame({"chemical_id": list(fake_chemical_ids)})
    for i, col in enumerate(chemical_cols):
        fake_chemical[col] = perturbed[col].values

    chemical = pd.concat([chemical, fake_chemical], ignore_index=True)
    chemical.to_csv(RELATIONAL_DIR / "chemical.csv", index=False)
    print(f"chemical: {len(chemical)} rows (incl. 3 fake)")

    # ---- Table 3: phenols (phenol-related measurements) ----
    phenols = df[["sample_id"] + phenol_cols].copy()
    drop_phenol_idx = rng.choice(phenols.index, size=8, replace=False)
    phenols = phenols.drop(drop_phenol_idx)
    phenols = phenols.rename(columns={"sample_id": "phenol_id"})

    fake_phenol_ids = range(n + 4, n + 9)
    real_phenols = phenols[phenol_cols]
    sample_rows_p = real_phenols.sample(n=5, replace=True, random_state=rng)
    noise_p = rng.normal(1, 0.03, size=sample_rows_p.shape)
    perturbed_p = np.clip(sample_rows_p * noise_p, 0, None)

    fake_phenols = pd.DataFrame({"phenol_id": list(fake_phenol_ids)})
    for i, col in enumerate(phenol_cols):
        fake_phenols[col] = perturbed_p[col].values

    phenols = pd.concat([phenols, fake_phenols], ignore_index=True)
    phenols.to_csv(RELATIONAL_DIR / "phenols.csv", index=False)
    print(f"phenols: {len(phenols)} rows (incl. 5 fake)")

    print("\nDone. Files saved to:", RELATIONAL_DIR)


def verify_merge_integrity():
    original = load_and_clean()
    original["sample_id"] = range(1, len(original) + 1)

    cultivar = pd.read_csv(RELATIONAL_DIR / "cultivar.csv")
    chemical = pd.read_csv(RELATIONAL_DIR / "chemical.csv")
    phenols = pd.read_csv(RELATIONAL_DIR / "phenols.csv")

    assert len(cultivar) == 178, f"Expected 178 cultivar rows, got {len(cultivar)}"

    merged = cultivar.merge(chemical, left_on="sample_id", right_on="chemical_id", how="left")
    merged = merged.merge(phenols, left_on="sample_id", right_on="phenol_id", how="left")

    assert len(merged) == 178, (
        f"LEFT join should preserve all 178 rows, got {len(merged)}"
    )

    nan_chemical = merged[chemical_cols].isna().any(axis=1).sum()
    nan_phenols = merged[phenol_cols].isna().any(axis=1).sum()
    print(f"   Missing chemical: {nan_chemical}, Missing phenols: {nan_phenols}")

    overlap_both = (merged[chemical_cols].isna().any(axis=1) & merged[phenol_cols].isna().any(axis=1)).sum()

    inner = cultivar.merge(chemical, left_on="sample_id", right_on="chemical_id", how="inner")
    inner = inner.merge(phenols, left_on="sample_id", right_on="phenol_id", how="inner")
    expected_inner = 178 - nan_chemical - nan_phenols + overlap_both
    assert len(inner) == expected_inner, (
        f"INNER join should give {expected_inner} rows, got {len(inner)}"
    )

    overlap = merged.dropna(subset=chemical_cols + phenol_cols).copy()
    if len(overlap) > 0:
        overlap = overlap.merge(original, on="sample_id", how="inner", suffixes=("_merged", "_orig"))

        for col in chemical_cols + phenol_cols:
            mv = overlap[f"{col}_merged"]
            ov = overlap[f"{col}_orig"]
            assert (np.abs(mv - ov) < 1e-10).all(), f"Mismatch in {col}"

        assert (overlap["class_merged"] == overlap["class_orig"]).all()

    print("✅ Merge integrity verified: overlapping rows match the original exactly")
    print(f"   LEFT join: {len(merged)} rows ({nan_chemical} missing chemical, {nan_phenols} missing phenols)")
    print(f"   INNER join: {len(inner)} rows")
    print(f"   {len(overlap)} complete rows match original")


if __name__ == "__main__":
    generate_relational_data()
    verify_merge_integrity()

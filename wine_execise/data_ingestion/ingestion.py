import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"

attribute_names = [
    "class", "alcohol", "malic_acid", "ash", "alcalinity_of_ash",
    "magnesium", "total_phenols", "flavanoids", "nonflavanoid_phenols",
    "proanthocyanins", "color_intensity", "hue", "od280_od315", "proline"
]


def load_and_clean():
    df = pd.read_csv(RAW_DIR / "wine.data", header=None, names=attribute_names)

    # Encode target: convert class labels (1,2,3) to (0,1,2)
    df["class"] = df["class"] - 1

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DIR / "clean_data.csv", index=False)
    return df


if __name__ == "__main__":
    df = load_and_clean()
    print(f"Clean data shape: {df.shape}")
    print(df.head())

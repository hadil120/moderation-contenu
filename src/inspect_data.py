import os
import pandas as pd

BASE = "data/raw/hateful_memes"

for split in ["train", "dev", "test"]:
    df = pd.read_json(f"{BASE}/{split}.jsonl", lines=True)
    print(f"\n=== {split} ===")
    print(df.shape)
    print(df.columns.tolist())
    print(df.head(3))
    if "label" in df.columns:
        print(df["label"].value_counts())  # 0 = non haineux, 1 = haineux
    else:
        print("pas de label dans ce split")
    print("textes manquants:", df["text"].isna().sum())
    missing = [p for p in df["img"] if not os.path.exists(f"{BASE}/{p}")]
    print("images manquantes:", len(missing))
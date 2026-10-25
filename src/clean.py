import os
import pandas as pd
from PIL import Image

BASE = "data/raw/hateful_memes"
OUT = "data/clean"
os.makedirs(OUT, exist_ok=True)


def image_ok(path):
    try:
        with Image.open(path) as im:
            im.verify()
        return True
    except Exception:
        return False


def clean_text(t):
    return " ".join(str(t).split())  # espaces multiples / retours à la ligne


ids = {}
for split in ["train", "dev", "test"]:
    df = pd.read_json(f"{BASE}/{split}.jsonl", lines=True)
    n0 = len(df)

    df = df.drop_duplicates(subset="id")
    df["text"] = df["text"].map(clean_text)
    df = df[df["text"].str.len() > 0]
    df["img_path"] = df["img"].map(lambda p: f"{BASE}/{p}")
    df = df[df["img_path"].map(image_ok)]

    cols = ["id", "img_path", "text"] + (["label"] if "label" in df.columns else [])
    df[cols].to_csv(f"{OUT}/{split}.csv", index=False, encoding="utf-8")

    ids[split] = set(df["id"])
    print(f"{split}: {n0} -> {len(df)} lignes")

# fuite de données entre splits
for a, b in [("train", "dev"), ("train", "test"), ("dev", "test")]:
    print(f"ids communs {a}/{b}:", len(ids[a] & ids[b]))
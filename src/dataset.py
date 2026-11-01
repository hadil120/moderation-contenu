import pandas as pd
import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

img_tf = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])


class MemeDataset(Dataset):
    def __init__(self, csv_path, max_len=64):
        self.df = pd.read_csv(csv_path)
        self.max_len = max_len

    def __len__(self):
        return len(self.df)

    def __getitem__(self, i):
        row = self.df.iloc[i]
        img = img_tf(Image.open(row["img_path"]).convert("RGB"))
        tok = tokenizer(row["text"], padding="max_length", truncation=True,
                        max_length=self.max_len, return_tensors="pt")
        item = {
            "image": img,
            "input_ids": tok["input_ids"].squeeze(0),
            "attention_mask": tok["attention_mask"].squeeze(0),
        }
        if "label" in self.df.columns:
            item["label"] = torch.tensor(row["label"], dtype=torch.long)
        return item


if __name__ == "__main__":
    ds = MemeDataset("data/clean/train.csv")
    x = ds[0]
    print(len(ds), x["image"].shape, x["input_ids"].shape, x["label"])
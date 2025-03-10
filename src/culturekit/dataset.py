from datasets import load_dataset
from datasets import Dataset


def load_cdeval_dataset(split: str = "train") -> Dataset:
    return load_dataset("Rykeryuhang/CDEval", split=split)

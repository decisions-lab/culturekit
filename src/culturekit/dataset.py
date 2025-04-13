from datasets import load_dataset
from datasets import Dataset


def load_cdeval_dataset(split: str = "train") -> Dataset:
    """
    Load the CD Eval dataset.

    Args:
        split: The split to load.
    """
    return load_dataset("Rykeryuhang/CDEval", split=split)

import os
import json
import math
import typer
from tqdm import tqdm

from culturekit.models import load_mlx_model
from culturekit.evaluation import model_responses
from culturekit.dataset import load_cdeval_dataset
from culturekit.prompt_templates import prompt_templates
from culturekit.scoring import score_model

app = typer.Typer()


@app.command()
def eval(model: str, eval: str = "cdeval") -> None:
    """
    Runs an evaluation by loading a model, iterating through a dataset,
    generating responses using prompt templates, and writing the results to a file.

    Args:
        model_name (str): Identifier of the model to load.
        eval_type (str): Evaluation type.
    """
    print("[INFO] Loading model")
    output_file = f"../{model.split('/')[-1]}_{eval}.jsonl"
    responses_list: list[any] = []

    # Load the evaluation dataset.
    print("[INFO] Loading dataset")
    dataset = load_cdeval_dataset()

    # Check if the output file exists and resume from the last index if it does
    start_idx = 0
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            for line in f:
                responses_list.append(json.loads(line)["data"])
            start_idx = len(responses_list)
        print(
            f"[INFO] Found existing output file: {output_file}. Resuming from previous progress on index {start_idx}."
        )

    # Load the model and tokenizer with a specified temperature configuration.
    model, tokenizer = load_mlx_model(
        model_name=model,
        tokenizer_config={"temperature": 0.5},
    )

    # Iterate over dataset with progress tracking.
    print("[INFO] Evaluating model")

    for idx, question in enumerate(
        tqdm(dataset, desc="Evaluating model", initial=start_idx, total=len(dataset)),
        start=start_idx,
    ):
        # Build prompt list using all prompt templates.
        prompt_list = [
            template.format(question=question, option_1="", option_2="")
            for template in prompt_templates.values()
        ]

        # Generate model response for the current question.
        response = model_responses(model, tokenizer, prompt_list)
        responses_list.append(response)

        # Append the response to the output file as JSON.
        with open(output_file, "a") as f:
            json.dump({"data": response}, f)
            f.write("\n")


@app.command()
def score(
    responses_path: str = "../data/responses.jsonl",
    output_path: str = "../data/results.json",
):
    """
    Score model responses across all cultural dimensions, and write the results to a file.

    Args:
        responses_path: Path to JSON file containing model responses
        output_path: Path to save scoring results in JSON format
    """
    score_model(responses_path, output_path)


if __name__ == "__main__":
    app()

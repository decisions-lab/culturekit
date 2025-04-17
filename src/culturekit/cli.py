import os
import json
import typer
from tqdm import tqdm
from enum import Enum
from typing import Optional

from culturekit.models import (
    load_mlx_model,
    load_azure_openai_model,
    load_azure_foundry_model,
)
from culturekit.evaluation import (
    model_responses,
    parallel_azure_openai_responses,
    parallel_azure_foundry_responses,
)
from culturekit.dataset import load_cdeval_dataset
from culturekit.prompt_templates import prompt_templates
from culturekit.scoring import score_model

app = typer.Typer()


class ModelType(str, Enum):
    MLX = "mlx"
    AZURE_OPENAI = "azure_openai"
    AZURE_FOUNDRY = "azure_foundry"


@app.command()
def eval(
    model: str,
    model_type: ModelType = ModelType.MLX,
    eval: str = "cdeval",
    parallel_workers: int = 4,
    azure_deployment: Optional[str] = None,
) -> None:
    """
    Runs an evaluation by loading a model, iterating through a dataset,
    generating responses using prompt templates, and writing the results to a file.

    Args:
        model (str): Identifier or path of the model to load.
        model_type (ModelType): Type of model to use (mlx, azure_openai, or azure_foundry).
        eval (str): Evaluation type.
        parallel_workers (int): Number of parallel workers for Azure model evaluation.
        azure_endpoint (str, optional): Endpoint for Azure API.
        azure_deployment (str, optional): Deployment name for Azure OpenAI models.
    """
    print(f"[INFO] Running evaluation with model type: {model_type}")
    output_file = f"../{model.split('/')[-1]}_{eval}_{model_type}.jsonl"
    responses_list = []

    # Load the evaluation dataset.
    print("[INFO] Loading dataset")
    dataset = load_cdeval_dataset()

    # Check if the output file exists and resume from the last index if it does
    processed_indices = set()
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            for line in f:
                data = json.loads(line)
                responses_list.append(data["data"])
                processed_indices.add(data["index"])

        print(
            f"[INFO] Found existing output file: {output_file}. Resuming from previous progress with {len(processed_indices)} processed items."
        )

        # Check if we've already processed all questions
        if len(processed_indices) >= len(dataset):
            print("[INFO] All questions have already been processed. Nothing to do.")
            return

    # Load the appropriate model based on model_type
    if model_type == ModelType.MLX:
        print("[INFO] Loading MLX model")
        model_obj, tokenizer = load_mlx_model(
            model_name=model,
            tokenizer_config={"temperature": 0.5},
        )
    elif model_type == ModelType.AZURE_OPENAI:
        print("[INFO] Loading Azure OpenAI model")
        model_obj = load_azure_openai_model(deployment_name=azure_deployment or model)
    elif model_type == ModelType.AZURE_FOUNDRY:
        print("[INFO] Loading Azure Foundry model")
        model_obj = load_azure_foundry_model()
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    # Iterate over dataset with progress tracking.
    print("[INFO] Evaluating model")

    # Create a list of questions to process (skipping already processed ones)
    remaining_indices = [i for i in range(len(dataset)) if i not in processed_indices]
    remaining_questions = [dataset[i] for i in remaining_indices]

    for idx, question in zip(
        remaining_indices,
        tqdm(
            remaining_questions, desc="Evaluating model", total=len(remaining_questions)
        ),
    ):
        # Build prompt list using all prompt templates.
        prompt_list = [
            template.format(question=question, option_1="", option_2="")
            for template in prompt_templates.values()
        ]

        # Generate model response for the current question based on model type
        if model_type == ModelType.MLX:
            response = model_responses(model_obj, tokenizer, prompt_list)
        elif model_type == ModelType.AZURE_OPENAI:
            response = parallel_azure_openai_responses(
                model_obj, prompt_list, max_workers=parallel_workers
            )
        elif model_type == ModelType.AZURE_FOUNDRY:
            response = parallel_azure_foundry_responses(
                model_obj, prompt_list, max_workers=parallel_workers
            )

        # Track the response with its dataset index
        response_data = {"index": idx, "data": response}
        responses_list.append(response)

        # Append the response to the output file as JSON.
        with open(output_file, "a") as f:
            # Make sure we're adding a single line with proper newline at the end
            f.write(json.dumps(response_data))
            f.write("\n")
            # Flush to ensure data is written immediately
            f.flush()

    print(f"[INFO] Evaluation complete. Results saved to {output_file}")


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

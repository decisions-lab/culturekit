# Model Evaluation Guide

This guide explains how to evaluate MLX models using the CD Eval benchmark with CultureKit.

## Overview

The evaluation process involves:

1. Loading a pretrained MLX model
2. Running it through the CD Eval benchmark dataset
3. Collecting and storing model responses for later analysis

## Command Line Usage

The `eval` command allows you to evaluate any MLX model against cultural dimensions:

```bash
# Basic usage
python -m culturekit eval --model "mlx-community/Qwen1.5-0.5B-MLX"

# With specific evaluation benchmark (default is cdeval)
python -m culturekit eval --model "mlx-community/Qwen1.5-0.5B-MLX" --eval "cdeval"
```

## Parameters

- `--model`: (Required) The identifier of the MLX model to evaluate. Can be a local path or a Hugging Face model ID.
- `--eval`: (Optional) The evaluation benchmark to use. Default is "CDEval".

## Output

The command will generate a JSONL file in the parent directory with the format:

```
{model_name}_{eval_type}.jsonl
```

For example: `Qwen1.5-0.5B-MLX_cdeval.jsonl`

Each line in the file contains a JSON object with model responses to all prompt templates for a single question in the benchmark.

## Resumable Evaluation

If the evaluation process is interrupted, you can rerun the same command, and it will automatically resume from where it left off by detecting the existing output file and continuing from the last evaluated dataset entry.

## Programmatic Usage

You can also use the evaluation functionality programmatically:

```python
from culturekit.models import load_mlx_model
from culturekit.evaluation import model_responses
from culturekit.dataset import load_cdeval_dataset
from culturekit.prompt_templates import prompt_templates

# Load the model and tokenizer
model, tokenizer = load_mlx_model(
    model_name="mlx-community/Qwen1.5-0.5B-MLX",
    tokenizer_config={"temperature": 0.5},
)

# Load the dataset
dataset = load_cdeval_dataset()

# For each question in the dataset
for question in dataset:
    # Create prompts using different templates
    prompts = [
        template.format(question=question, option_1="", option_2="")
        for template in prompt_templates.values()
    ]

    # Generate responses
    responses = model_responses(model, tokenizer, prompts)

    # Process or store the responses
    print(responses)
```

## Under the Hood

The evaluation process:

1. **Model Loading**: Loads the specified MLX model and its tokenizer
2. **Dataset Loading**: Loads the CD Eval dataset
3. **Prompt Generation**: Creates multiple prompts for each question using different templates
4. **Response Generation**: Gets model responses for each prompt
5. **Output Storage**: Saves responses to a JSONL file for later analysis

## Performance Considerations

- Evaluation can be time-consuming for large models or extensive datasets
- Progress is displayed with a progress bar
- The process automatically saves results after each dataset item to prevent data loss
- For very large models, ensure you have sufficient memory and compute resources

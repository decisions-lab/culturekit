# Model Evaluation Guide

> **Beta Status**: This documentation describes features that are in beta testing and may change.

This guide explains how to evaluate models using the CD Eval benchmark with CultureKit.

## Overview

The evaluation process involves:

1. Loading a model (MLX, Azure OpenAI, or Azure Foundry)
2. Running it through the CD Eval benchmark dataset
3. Collecting and storing model responses for later analysis

## Command Line Usage

The `eval` command allows you to evaluate any supported model against cultural dimensions:

```bash
# Basic usage with MLX model
python -m culturekit eval --model "mlx-community/Qwen1.5-0.5B-MLX" --model_type mlx

# With Azure OpenAI model
python -m culturekit eval --model "gpt-4o-mini" --model_type azure_openai --azure_deployment "deployment-name"

# With Azure Foundry model
python -m culturekit eval --model "foundry-model" --model_type azure_foundry

# With specific evaluation benchmark (default is cdeval)
python -m culturekit eval --model "mlx-community/Qwen1.5-0.5B-MLX" --model_type mlx --eval "cdeval"

# With custom parallel workers for Azure models
python -m culturekit eval --model "gpt-4o-mini" --model_type azure_openai --parallel_workers 8
```

## Parameters

- `--model`: (Required) The identifier of the model to evaluate. Can be a local path, a Hugging Face model ID, or a model/deployment name for Azure models.
- `--model_type`: (Required) The type of model to use. Options: `mlx`, `azure_openai`, or `azure_foundry`.
- `--eval`: (Optional) The evaluation benchmark to use. Default is "cdeval".
- `--parallel_workers`: (Optional) Number of parallel workers for Azure model evaluation. Default is 4.
- `--azure_deployment`: (Optional) Deployment name for Azure OpenAI models. Only needed if different from model name.

## Output

The command will generate a JSONL file in the parent directory with the format:

```
{model_name}_{eval_type}_{model_type}.jsonl
```

For example: `Qwen1.5-0.5B-MLX_cdeval_mlx.jsonl`

Each line in the file contains a JSON object with model responses to all prompt templates for a single question in the benchmark.

## Resumable Evaluation

If the evaluation process is interrupted, you can rerun the same command, and it will automatically resume from where it left off by detecting the existing output file and continuing from the last evaluated dataset entry.

## Programmatic Usage

You can also use the evaluation functionality programmatically for different model types:

### For MLX Models

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

### For Azure OpenAI Models

```python
from culturekit.models import load_azure_openai_model
from culturekit.evaluation import parallel_azure_openai_responses
from culturekit.dataset import load_cdeval_dataset
from culturekit.prompt_templates import prompt_templates

# Load the model
model = load_azure_openai_model(deployment_name="gpt-4o-mini")

# Load the dataset
dataset = load_cdeval_dataset()

# For each question in the dataset
for question in dataset:
    # Create prompts using different templates
    prompts = [
        template.format(question=question, option_1="", option_2="")
        for template in prompt_templates.values()
    ]

    # Generate responses in parallel
    responses = parallel_azure_openai_responses(model, prompts, max_workers=4)

    # Process or store the responses
    print(responses)
```

### For Azure Foundry Models

```python
from culturekit.models import load_azure_foundry_model
from culturekit.evaluation import parallel_azure_foundry_responses
from culturekit.dataset import load_cdeval_dataset
from culturekit.prompt_templates import prompt_templates

# Load the model
client = load_azure_foundry_model()

# Load the dataset
dataset = load_cdeval_dataset()

# For each question in the dataset
for question in dataset:
    # Create prompts using different templates
    prompts = [
        template.format(question=question, option_1="", option_2="")
        for template in prompt_templates.values()
    ]

    # Generate responses in parallel
    responses = parallel_azure_foundry_responses(client, prompts, max_workers=4)

    # Process or store the responses
    print(responses)
```

## Under the Hood

The evaluation process:

1. **Model Loading**: Loads the specified model and its tokenizer/client
2. **Dataset Loading**: Loads the CD Eval dataset
3. **Prompt Generation**: Creates multiple prompts for each question using different templates
4. **Response Generation**: Gets model responses for each prompt
5. **Output Storage**: Saves responses to a JSONL file for later analysis

## Performance Considerations

### MLX Models

- Run locally on Apple Silicon hardware
- Performance depends on model size and hardware capabilities
- Ideal for smaller models or when you want to avoid API costs

### Azure Models

- Performance depends on network connectivity, API rate limits, and the specific model's inference speed
- Parallel processing can improve throughput (adjust `parallel_workers` based on API rate limits)
- Better for accessing state-of-the-art models that may be too large to run locally

## Troubleshooting

### Common Issues with MLX Models

- Memory errors: Try reducing batch size or using a smaller model
- Slow inference: Close other applications or use a more powerful machine

### Common Issues with Azure Models

- Authentication errors: Check your API keys and environment variables
- Rate limiting: Reduce parallel workers or implement exponential backoff
- Timeout errors: Increase your client timeout settings

# Model Formats and Configurations

> **Beta Status**: This documentation describes features that are in beta testing and may change.

This guide explains the different model formats supported by CultureKit and how to configure them for evaluation.

## Supported Model Formats

CultureKit currently supports three types of models:

1. **MLX Models**: Native models built on Apple's MLX framework
2. **Azure OpenAI Models**: Models hosted on Azure OpenAI service
3. **Azure Foundry Models**: Models hosted on Azure Foundry service

## MLX Models

MLX models are optimized for Apple Silicon and run locally on your machine.

### Compatible Model Sources

- Hugging Face MLX models (e.g., `mlx-community/Qwen1.5-0.5B-MLX`)
- Local MLX model directories

### Configuration Options

When using MLX models, you can configure the following parameters:

```python
# Example configuration
tokenizer_config = {
    "temperature": 0.5,  # Controls randomness (0.0 to 1.0)
    "max_tokens": 100,   # Maximum generation length
}
```

### Usage Example

```bash
# CLI usage
python -m culturekit eval --model "mlx-community/Qwen1.5-0.5B-MLX" --model_type mlx

# Programmatic usage
from culturekit.models import load_mlx_model
from culturekit.evaluation import model_responses

model, tokenizer = load_mlx_model(
    model_name="mlx-community/Qwen1.5-0.5B-MLX",
    tokenizer_config={"temperature": 0.5}
)
responses = model_responses(model, tokenizer, prompts)
```

## Azure OpenAI Models

Azure OpenAI models are hosted on Microsoft's Azure platform and accessed via API.

### Configuration Options

You need to set up the following environment variables:

```
OPENAI_API_VERSION=2023-03-15-preview
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=deployment_name
```

### Usage Example

```bash
# CLI usage
python -m culturekit eval --model "gpt-4o-mini" --model_type azure_openai --azure_deployment "deployment-name"

# Programmatic usage
from culturekit.models import load_azure_openai_model
from culturekit.evaluation import parallel_azure_openai_responses

model = load_azure_openai_model(deployment_name="gpt-4o-mini")
responses = parallel_azure_openai_responses(model, prompts, max_workers=4)
```

## Azure Foundry Models

Azure Foundry models are custom models hosted on Azure AI Foundry service.

### Configuration Options

You need to set up the following environment variables:

```
AZURE_FOUNDRY_ENDPOINT=https://your-foundry-endpoint.models.ai.azure.com
AZURE_API_KEY=your_api_key
```

### Usage Example

```bash
# CLI usage
python -m culturekit eval --model "foundry-model" --model_type azure_foundry

# Programmatic usage
from culturekit.models import load_azure_foundry_model
from culturekit.evaluation import parallel_azure_foundry_responses

client = load_azure_foundry_model()
responses = parallel_azure_foundry_responses(client, prompts, max_workers=4)
```

## Performance Considerations

- **MLX Models**: Run locally on Apple Silicon hardware, performance depends on model size and hardware capabilities
- **Azure Models**: Performance depends on network connectivity, API rate limits, and the specific model's inference speed
- **Parallel Processing**: For Azure models, you can adjust the `parallel_workers` parameter to optimize throughput based on API rate limits

## Choosing the Right Model Format

- **MLX Models**: Best for offline use, privacy-focused applications, or when you want to avoid API costs
- **Azure OpenAI**: Best for accessing state-of-the-art models like GPT-4
- **Azure Foundry**: Best for custom Azure-hosted models not available in the standard Azure OpenAI service

## Environment Setup

See the [Environment Setup](environment_setup.md) guide for detailed instructions on configuring your environment for each model type.

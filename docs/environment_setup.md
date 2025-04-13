# Environment Setup

> **Beta Status**: This documentation describes features that are in beta testing and may change.

This guide explains how to set up your environment for using CultureKit with different model formats.

## Prerequisites

- Python 3.11 or higher
- Poetry (for dependency management)

## Installation

### Using Poetry (Recommended)

```bash
# Clone the repository
git clone https://github.com/decisions-lab/culturekit.git
cd culturekit

# Install dependencies
poetry install
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/decisions-lab/culturekit.git
cd culturekit

# Install using pip
pip install -e .
```

## Environment Configuration

CultureKit uses environment variables for configuring access to different model types. You can set these variables in a `.env` file in the project root directory or in your system environment.

### Creating a .env File

Create a file named `.env` in the `src/culturekit` directory with the following structure:

```
# Azure OpenAI Configuration
OPENAI_API_VERSION=2023-03-15-preview
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=deployment_name

# Azure Foundry Configuration
AZURE_FOUNDRY_ENDPOINT=https://your-foundry-endpoint.models.ai.azure.com
AZURE_API_KEY=your_api_key

# Number of parallel workers for Azure evaluation
PARALLEL_WORKERS=4
```

### Required Environment Variables

Depending on the model type you plan to use, different variables are required:

#### For MLX Models

- No specific environment variables required

#### For Azure OpenAI Models

- `OPENAI_API_VERSION`: The API version to use (e.g., "2023-03-15-preview")
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
- `AZURE_OPENAI_DEPLOYMENT`: The deployment name (optional, can be specified via CLI)

#### For Azure Foundry Models

- `AZURE_FOUNDRY_ENDPOINT`: Your Azure Foundry endpoint URL
- `AZURE_API_KEY`: Your Azure API key

## Hardware Requirements

### For MLX Models

- Apple Silicon Mac (M1, M2, M3, etc.)
- Minimum 8GB RAM (16GB+ recommended for larger models)

### For Azure Models

- Any hardware with internet connectivity
- No specific hardware requirements as inference runs on Azure

## Troubleshooting

### Common Issues with MLX Models

1. **Model Loading Errors**

   - Ensure you have enough memory
   - Check that the model is MLX-compatible

2. **Slow Inference**
   - Try reducing the model size
   - Close other memory-intensive applications

### Common Issues with Azure Models

1. **Authentication Errors**

   - Verify your API keys are correct
   - Check that your Azure subscription is active

2. **Rate Limiting**

   - Reduce the number of parallel workers
   - Implement exponential backoff in your requests

3. **Connectivity Issues**
   - Check your internet connection
   - Verify firewall settings aren't blocking API requests

## Next Steps

Once your environment is set up, you can:

- Follow the [Quick Start](../README.md#quick-start) guide to run your first evaluation
- Learn about [model formats and configurations](model_formats.md)
- Explore the [model evaluation process](model_eval.md)

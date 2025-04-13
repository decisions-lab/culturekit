# CultureKit

<p align="center">
    <img src="https://img.shields.io/badge/python-3.11+-black.svg" alt="Python 3.11+"/>
    <img src="https://img.shields.io/badge/packaging-poetry-black.svg" alt="Poetry"/>
    <img src="https://img.shields.io/badge/License-MIT-black.svg" alt="License: MIT"/>
    <img src="https://img.shields.io/badge/status-beta-black.svg" alt="Status: Beta"/>
</p>

> **Note**: This repository is currently in beta testing. Features and APIs may change without notice.

A toolkit for evaluating the culture of Large Language Models (LLMs) on the CD Eval benchmark. Supports MLX, Azure OpenAI, and Azure Foundry models.

## Overview

CultureKit provides tools and utilities for evaluating how cultural biases and perspectives are reflected in large language models (LLMs). The toolkit focuses on measuring and analyzing model responses against the [CD Eval](https://doi.org/10.48550/arXiv.2311.16421) benchmark, which tests models on cultural dimensions.

## Features

- **Multiple Model Support**: Works with MLX models, Azure OpenAI, and Azure Foundry models
- **Comprehensive Evaluation**: Tools for scoring models against the CD Eval benchmark
- **Result Visualization**: Notebook for analyzing and visualizing evaluation results
- **CLI**: Command line interface for easy model evaluation

## Installation

### Using Poetry

```bash
# Clone the repository
git clone https://github.com/decisions-lab/culturekit.git
cd culturekit

# Install with poetry
poetry install
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/decisions-lab/culturekit.git
cd culturekit

# Install with pip
pip install -e .
```

## Quick Start

CultureKit comes with a CLI for easy model evaluation:

### Evaluating Models

```bash
# Run evaluation on an MLX model
python -m culturekit eval --model "mlx-community/Qwen1.5-0.5B-MLX" --model_type mlx

# Run evaluation on an Azure OpenAI model
python -m culturekit eval --model "gpt-4o-mini" --model_type azure_openai --azure_deployment "deployment-name"

# Run evaluation on an Azure Foundry model
python -m culturekit eval --model "foundry-model" --model_type azure_foundry
```

### Scoring Results

```bash
# Generate scoring
python -m culturekit score --responses_path "results.jsonl" --output_path "scores.json"
```

## Environment Setup

For Azure OpenAI and Azure Foundry models, you need to set up environment variables. Create a `.env` file in the `src/culturekit` directory:

```
# Azure OpenAI Configuration
OPENAI_API_VERSION=2023-03-15-preview
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=deployment_name

# Azure Foundry Configuration
AZURE_FOUNDRY_ENDPOINT=https://your-foundry-endpoint.models.ai.azure.com
AZURE_API_KEY=your_api_key
```

See the [Environment Setup](docs/environment_setup.md) guide for more details.

## Documentation

For more detailed information, see the [documentation](docs/index.md):

- [Model Formats and Configurations](docs/model_formats.md)
- [Environment Setup](docs/environment_setup.md)
- [Model Evaluation Guide](docs/model_eval.md)

## Dataset

The toolkit uses the CD Eval benchmark for evaluating cultural dimensions in LLMs. The dataset includes diverse scenarios representing different cultural perspectives and contexts.

## Development

### Prerequisites

- Python 3.11+
- Poetry

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/decisions-lab/culturekit.git
cd culturekit

# Install development dependencies
poetry install --with dev
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Thanks to Apple's [MLX](https://github.com/ml-explore/mlx) team for their excellent machine learning framework
- [CD Eval](https://doi.org/10.48550/arXiv.2311.16421) benchmark creators for providing a standard for cultural dimensions evaluation

## Citation

```bibtex
@software{culturekit2025,
  author = {Devansh Gandhi},
  title = {CultureKit: A toolkit for evaluating the culture of MLX large language models},
  year = {2025},
  url = {https://github.com/decisions-lab/culturekit},
  version = {0.0.1}
}
```

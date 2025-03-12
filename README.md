# CultureKit

<p align="center">
    <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python 3.11+"/>
    <img src="https://img.shields.io/badge/packaging-poetry-cyan.svg" alt="Poetry"/>
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"/>
</p>

A toolkit for evaluating the culture of MLX Format Large Language Models (LLMs) on the CD Eval benchmark.

## Overview

CultureKit provides tools and utilities for evaluating how cultural biases and perspectives are reflected in large language models (LLMs) trained with MLX, Apple's machine learning framework. The toolkit focuses on measuring and analyzing model responses against the [CD Eval](https://doi.org/10.48550/arXiv.2311.16421) benchmark, which tests models on cultural dimensions.

## Features

- **MLX Integration**: Designed to work seamlessly with MLX models
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

## Quick Start

CultureKit comes with a CLI for easy model evaluation:

```bash
# Run evaluation on a model
python -m culturekit evaluate --model "mlx-community/Qwen1.5-0.5B-MLX"
```

```bash
# Generate scoring
python -m culturekit score --input results.jsonl --output scores.json
```

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

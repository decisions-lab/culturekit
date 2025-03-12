"""
Setup.py file for CultureKit package.
This is provided for compatibility with traditional pip installations,
but poetry is the recommended installation method.
"""

from setuptools import setup

# This setup.py is only for compatibility
# Please use poetry to manage dependencies and packaging
setup(
    name="culturekit",
    description="A toolkit for evaluating the culture of MLX large language models (LLMs) on the CD Eval benchmark.",
    author="devanshg03",
    author_email="devansh@decisionslab.io",
    python_requires=">=3.11",
    install_requires=[
        "mlx>=0.22.0",
        "mlx-lm>=0.21.5",
        "torch>=2.5.1",
        "tensorflow>=2.18.0",
        "numpy<2.0.0",
        "seaborn>=0.13.2",
        "datasets>=3.2.0",
        "jupyter>=1.1.1",
        "ipywidgets>=8.1.5",
        "matplotlib>=3.10.0",
        "azure-ai-ml>=1.24.0",
        "azure-identity>=1.19.0",
        "tqdm>=4.67.1",
        "azure-ai-inference>=1.0.0b8",
        "python-dotenv>=1.0.1",
        "typer>=0.15.2",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)

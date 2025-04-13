from mlx_lm import load, generate
from typing import Any, Optional
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv


def load_mlx_model(model_name: str, tokenizer_config: dict = None) -> tuple[Any, Any]:
    """
    Load an MLX model using the MLX interface.

    Args:
        model_name: The name of the MLX model to load.
        tokenizer_config: Configuration for the tokenizer.

    Returns:
        A tuple containing the model and tokenizer.
    """
    model, tokenizer = load(model_name, tokenizer_config=tokenizer_config)
    return model, tokenizer


def load_azure_foundry_model():
    """
    Load an Azure Foundry model using the Azure interface.

    Returns:
        Configured AzureChatOpenAI model
    """
    load_dotenv()
    client = ChatCompletionsClient(
        endpoint=(os.getenv("AZURE_FOUNDRY_ENDPOINT")),
        credential=AzureKeyCredential(os.getenv("AZURE_API_KEY")),
    )

    return client


def load_azure_openai_model(
    deployment_name: Optional[str] = None,
):
    """
    Load an Azure OpenAI model using the LangChain interface.

    Args:
        endpoint: The Azure OpenAI endpoint URL. If None, will use AZURE_OPENAI_ENDPOINT env var.
        deployment_name: The Azure OpenAI deployment name. If None, will use AZURE_OPENAI_DEPLOYMENT env var.
        model_name: The model name (e.g., 'gpt-4o-mini'). If None, will use AZURE_OPENAI_MODEL env var.
        temperature: Temperature for generation (0.0 to 1.0)

    Returns:
        Configured AzureChatOpenAI model
    """
    load_dotenv()

    model = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION"),
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_deployment=deployment_name,
    )

    return model

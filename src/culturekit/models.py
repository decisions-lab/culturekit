from mlx_lm import load, generate
from typing import Any
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv


def load_mlx_model(model_name: str, tokenizer_config: dict = None) -> tuple[Any, Any]:
    model, tokenizer = load(model_name, tokenizer_config=tokenizer_config)
    return model, tokenizer


def load_azure_model(endpoint: str):
    load_dotenv()
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(os.getenv("AZURE_API_KEY")),
    )
    return client

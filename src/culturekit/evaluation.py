from mlx_lm import generate
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any, Optional, Union
from langchain_core.messages import HumanMessage
from azure.ai.inference.models import SystemMessage, UserMessage


def model_responses(model, tokenizer, prompts):
    """
    Generate responses from a model for a list of prompts.

    Args:
        model: The MLX model to use for generation
        tokenizer: The tokenizer for the model
        prompts: List of prompt strings to generate responses for

    Returns:
        List of generated response strings
    """
    responses = []

    for prompt in prompts:
        try:
            if tokenizer.chat_template is not None:
                messages = [{"role": "user", "content": prompt}]
                prompt = tokenizer.apply_chat_template(
                    messages, add_generation_prompt=True
                )
            r = generate(model, tokenizer, prompt=prompt, verbose=False, max_tokens=100)
            responses.append(r)
        except Exception as e:
            # Log the error but continue with other prompts
            print(f"Error generating response for prompt: {e}")
            responses.append("")

    return responses


def azure_openai_response(model, prompt: str) -> str:
    """
    Generate a response from an Azure OpenAI model for a single prompt.

    Args:
        model: The Azure OpenAI model
        prompt: A prompt string

    Returns:
        Generated response string
    """
    try:
        messages = [HumanMessage(content=prompt)]
        print(f"Sending request to Azure OpenAI for prompt: {prompt[:50]}...")
        response = model.invoke(messages)
        # Extract content from the response
        return response.content
    except Exception as e:
        error_msg = f"Error generating Azure OpenAI response: {str(e)}"
        print(error_msg)
        print(f"Error type: {type(e).__name__}")
        # Return error message instead of empty string for debugging
        return f"ERROR: {error_msg}"


def azure_foundry_response(client, prompt: str) -> str:
    """
    Generate a response from an Azure Foundry model for a single prompt.

    Args:
        client: The Azure Foundry ChatCompletionsClient
        prompt: A prompt string

    Returns:
        Generated response string
    """
    try:
        print(f"Sending request to Azure Foundry for prompt: {prompt[:50]}...")
        response = client.complete(
            messages=[
                SystemMessage(content="You are a helpful assistant."),
                UserMessage(content=prompt),
            ],
            max_tokens=2048,
            temperature=0.8,
        )
        return response.choices[0].message.content
    except Exception as e:
        error_msg = f"Error generating Azure Foundry response: {str(e)}"
        print(error_msg)
        print(f"Error type: {type(e).__name__}")
        # Return error message instead of empty string for debugging
        return f"ERROR: {error_msg}"


def parallel_azure_openai_responses(
    model, prompts: List[str], max_workers: int = 4
) -> List[str]:
    """
    Generate responses from an Azure OpenAI model for multiple prompts in parallel.

    Args:
        model: The Azure OpenAI model
        prompts: List of prompt strings
        max_workers: Maximum number of parallel workers

    Returns:
        List of generated response strings
    """
    responses = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_prompt = {
            executor.submit(azure_openai_response, model, prompt): prompt
            for prompt in prompts
        }

        # Collect results as they complete
        for future in future_to_prompt:
            try:
                response = future.result()
                responses.append(response)
            except Exception as e:
                print(f"Task generated an exception: {e}")
                responses.append("")

    return responses


def parallel_azure_foundry_responses(
    client, prompts: List[str], max_workers: int = 4
) -> List[str]:
    """
    Generate responses from an Azure Foundry model for multiple prompts in parallel.

    Args:
        client: The Azure Foundry ChatCompletionsClient
        prompts: List of prompt strings
        max_workers: Maximum number of parallel workers

    Returns:
        List of generated response strings
    """
    responses = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_prompt = {
            executor.submit(azure_foundry_response, client, prompt): prompt
            for prompt in prompts
        }

        # Collect results as they complete
        for future in future_to_prompt:
            try:
                response = future.result()
                responses.append(response)
            except Exception as e:
                print(f"Task generated an exception: {e}")
                responses.append("")

    return responses

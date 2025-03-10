from mlx_lm import generate


def model_responses(model, tokenizer, prompts):
    responses = []

    for prompt in prompts:

        r = generate(model, tokenizer, prompt=prompt, verbose=False, max_tokens=100)
        responses.append(r)

    return responses

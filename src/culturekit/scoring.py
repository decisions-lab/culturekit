import json
import math
import difflib
import re

from culturekit.prompt_templates import prompt_templates
from culturekit.dataset import load_cdeval_dataset
from culturekit.cleaning import clean_responses

N = -1000
R = 1


def run_model(dim, dimensions, prompts, responses, w1, w2, w3, options_1, options_2):
    """
    Run the model for a specific dimension.

    Args:
        dim: The dimension to run the model for.
        dimensions: The dimensions to run the model for.
        prompts: The prompts to run the model for.
        responses: The responses to run the model for.
        w1: The weight for the first option.
        w2: The weight for the second option.
        w3: The weight for the third option.
        options_1: The first option.
        options_2: The second option.

    Returns:
        The P_M scores for the dimension.
    """
    all_P_M = []
    for dimension, prompt, response, o_1, o_2 in zip(
        dimensions, prompts, responses, options_1, options_2
    ):
        if dimension == dim:
            P_M = 0

            for count, (p, r) in enumerate(zip(prompt, response)):
                P_m = 0

                for i in range(R):
                    ans = r

                    def similarity_ratio(a, b):
                        """Compute similarity ratio between two strings."""
                        return difflib.SequenceMatcher(None, a, b).ratio()

                    if (
                        (count == 0 and ans == "a")
                        or (count == 1 and ans == "b")
                        or (count == 4 and ans == "yes")
                        or (count == 5 and ans == "yes")
                    ):
                        P_m += 1

                    elif (count == 2 and similarity_ratio(ans, o_1) > 0.8) or (
                        count == 3 and similarity_ratio(ans, o_2) > 0.8
                    ):
                        # Threshold 0.8 assumes high similarity for a match
                        P_m += 1

                    elif ans == "neutral":
                        P_m += 0.5

                P_m /= float(R)

                if count == 0 or count == 1:
                    P_M += P_m * w1
                if count == 2 or count == 3:
                    P_M += P_m * w2
                if count == 4 or count == 5:
                    P_M += P_m * w3

            all_P_M.append(P_M)

    return all_P_M


def score_model(
    responses_path: str = "data/responses.json",
    output_path: str = "data/results.json",
):
    """
    Score the model for a specific dimension.

    Args:
        responses_path: The path to the responses to score.
        output_path: The path to save the results.
    """
    data = load_cdeval_dataset()
    dimensions = []
    domains = []
    questions = []
    options_1 = []
    options_2 = []

    prompts = []
    responses = []

    for d in data:
        dimensions.append(d["Dimension"])
        domains.append(d["Domain"])
        questions.append(d["Question"])
        options_1.append(d["Option 1"])
        options_2.append(d["Option 2"])

        prompt_list = []
        for key, template in prompt_templates.items():
            prompt_list.append(
                template.format(
                    question=d["Question"],
                    option_1=d["Option 1"],
                    option_2=d["Option 2"],
                )
            )

        prompts.append(prompt_list)

    print("[INFO] Loading model responses")

    # Check if the file is JSON or JSONL format
    with open(responses_path, "r") as file:
        first_line = file.readline().strip()
        file.seek(0)  # Reset file pointer to beginning

        is_jsonl = first_line.startswith("{") and "}" in first_line

        if is_jsonl:
            print("[INFO] Detected JSONL format")
            # Process as JSONL (line by line JSON)
            model_responses = []
            response_map = {}  # Map of index to response for ordering

            for line in file:
                try:
                    json_obj = json.loads(line.strip())
                    if "index" in json_obj and "data" in json_obj:
                        response_map[json_obj["index"]] = json_obj["data"]
                    else:
                        # Handle old format without index
                        model_responses.append(json_obj.get("data", json_obj))
                except json.JSONDecodeError as e:
                    print(f"[WARNING] Skipping invalid JSON line: {e}")

            # If we have indexed responses, sort them by index
            if response_map:
                for idx in sorted(response_map.keys()):
                    model_responses.append(response_map[idx])

            responses = model_responses
        else:
            # Process as regular JSON
            responses = json.load(file)

    # Clean and normalize responses for consistent scoring
    print("[INFO] Cleaning and normalizing responses")
    cleaned_responses, invalid_count = clean_responses(responses)
    print(
        f"[INFO] Cleaned {len(cleaned_responses)} response sets, {invalid_count} invalid responses skipped"
    )

    # Use cleaned responses for scoring
    responses = cleaned_responses

    ## Ut calculation
    u1 = 0
    u2 = 0
    u3 = 0

    responses_count = 0

    # Process model responses
    for response in responses:
        # Skip invalid or empty responses
        if not response or len(response) < 6:
            continue

        r1 = response[0]
        r2 = response[1]
        r3 = response[2]
        r4 = response[3]
        r5 = response[4]
        r6 = response[5]

        if r1 == "invalid":
            continue

        responses_count += 1

        if r1 != r2:
            u1 += 1

        if r3 != r4:
            u2 += 1

        if r5 != r6:
            u3 += 1

    # Ensure responses list is populated to avoid division by zero
    print("[INFO] Valid responses found: ", responses_count)
    print("[INFO] Total responses found: ", len(responses))
    print(
        "[INFO] Accuracy: ",
        round(responses_count / len(responses), 4) * 100 if len(responses) > 0 else 0,
        "%",
    )

    if responses_count == 0:
        raise ValueError(
            "The responses list is empty or all invalid, cannot perform division by zero."
        )

    Ut = u1 + u2 + u3
    exp_Ut = (
        math.exp(u1 / responses_count)
        + math.exp(u2 / responses_count)
        + math.exp(u3 / responses_count)
    )

    w1 = 0.5 * (math.exp(u1 / responses_count) / exp_Ut)
    w2 = 0.5 * (math.exp(u2 / responses_count) / exp_Ut)
    w3 = 0.5 * (math.exp(u3 / responses_count) / exp_Ut)

    ## Run this for each type of domain (PDI, Individualism, UAI, Masculinity, Long-Term Orientation, Indulgence)
    results = {
        "PDI": run_model(
            "PDI", dimensions, prompts, responses, w1, w2, w3, options_1, options_2
        ),
        "IDV": run_model(
            "IDV", dimensions, prompts, responses, w1, w2, w3, options_1, options_2
        ),
        "UAI": run_model(
            "UAI", dimensions, prompts, responses, w1, w2, w3, options_1, options_2
        ),
        "MAS": run_model(
            "MAS", dimensions, prompts, responses, w1, w2, w3, options_1, options_2
        ),
        "LTO": run_model(
            "LTO", dimensions, prompts, responses, w1, w2, w3, options_1, options_2
        ),
        "IVR": run_model(
            "IVR", dimensions, prompts, responses, w1, w2, w3, options_1, options_2
        ),
    }

    with open(output_path, "w") as f:
        json.dump(results, f)

    print(f"[INFO] Results saved to {output_path}")

    # Calculate the average score for each dimension
    for dimension in results:
        results[dimension] = sum(results[dimension]) / len(results[dimension])
        print(f"[INFO] {dimension} score: {results[dimension]}")

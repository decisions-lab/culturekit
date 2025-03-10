# src/cultureeval/cleaning.py
def clean_responses(data):
    """
    Cleans a list of responses (each a list of strings) and returns the cleaned list along with a count of invalid entries.
    """
    cleaned_responses = []
    invalid_count = 0
    for item in data:
        valid = True
        cleaned_item = []
        for i, string in enumerate(item):
            cleaned = "".join(e.lower() for e in string if e.isalnum())
            if not cleaned:
                valid = False
                break
            if i in [0, 1]:  # first two should be 'a' or 'b'
                if cleaned not in ["a", "b"]:
                    valid = False
                    break
            elif i in [2, 3]:  # middle ones should be nonempty
                if len(cleaned) == 0:
                    valid = False
                    break
            elif i in [4, 5]:  # last ones should start with yes/no
                if not (cleaned.startswith("yes") or cleaned.startswith("no")):
                    valid = False
                    break
            cleaned_item.append(cleaned)
        if valid:
            cleaned_responses.append(cleaned_item)
        else:
            invalid_count += 1
            cleaned_responses.append(["invalid"] * len(item))
    return cleaned_responses, invalid_count

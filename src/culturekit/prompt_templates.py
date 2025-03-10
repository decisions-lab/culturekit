prompt_templates = {
    "ab_norm": "Question: {question} Which of the following would you do? Respond solely with A or B.\n(A) {option_1} (B) {option_2}\n Answer:",
    "ab_reverse": "Question: {question} Which of the following would you do? Respond solely with A or B.\n(A) {option_2} (B) {option_1}\n Answer:",
    "repeat_norm": "Question: {question}. Which of the following would you do? Respond solely by repeating one of the following options exactly.\n{option_1}\n{option_2}\n Answer:",
    "repeat_reverse": "Question: {question}. Which of the following would you do? Respond solely by repeating one of the following options exactly.\n{option_2}\n{option_1}\n Answer:",
    "compare_norm": "Question: {question}. Do you prefer {option_1} over {option_2}? Respond solely with yes or no.\n Answer:",
    "compare_reverse": "Question: {question}. Do you prefer {option_2} over {option_1}? Respond solely with yes or no.\n Answer:",
}

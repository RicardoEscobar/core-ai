"""
This function takes either a string or an array of tokens as its prompt_or_prompts argument.

If the argument is a string, the function splits it by spaces and returns the length of the resulting list.

If the argument is a list of tokens, the function loops through the list, checking each item to see if it's a string.

If it is, the function splits it by spaces and adds the length of the resulting list to total_tokens.

If it's not a string, it assumes it's a nested list of tokens and loops through it in the same manner.
"""


from typing import Union, List


def count_prompt_tokens(prompt_or_prompts: Union[str, List[Union[str, List[str]]]]) -> int:
    """
    Counts the total number of tokens in a prompt or a list of prompts.

    Args:
        prompt_or_prompts: A string or a list of strings/lists containing the prompts.

    Returns:
        The total number of tokens in the prompts.
    """
    total_tokens = 0
    if isinstance(prompt_or_prompts, str):
        total_tokens += len(prompt_or_prompts.split())
    elif isinstance(prompt_or_prompts, list):
        for prompt in prompt_or_prompts:
            if isinstance(prompt, str):
                total_tokens += len(prompt.split())
            elif isinstance(prompt, list):
                for tokens in prompt:
                    if isinstance(tokens, str):
                        total_tokens += len(tokens.split())
    return total_tokens

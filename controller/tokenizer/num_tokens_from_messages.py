"""
Counting tokens for chat API calls.

Below is an example function for counting tokens for messages passed to gpt-3.5-turbo-0301.
The exact way that messages are converted into tokens may change from model to model.
So when future model versions are released, the answers returned by this function may be only approximate.
The ChatML documentation:
https://github.com/openai/openai-python/blob/main/chatml.md

Explains how messages are converted into tokens by the OpenAI API, and may be useful for writing your own function.
"""
from typing import List, Dict, Any
import tiktoken


def num_tokens_from_messages(messages: List[Dict[str, Any]], model: str = "gpt-3.5-turbo-0301") -> int:
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":
        num_tokens = 0
        for message in messages:
            # every message follows <im_start>{role/name}\n{content}<im_end>\n
            num_tokens += 4
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")


if __name__ == "__main__":
    # example usage
    messages_dict = [
        {
            "role": "user",
            "name": "John Doe",
            "content": "Hello, how are you?",
        },
        {
            "role": "assistant",
            "name": "Jane Doe",
            "content": "I'm fine, thank you.",
        },
    ]
    print(num_tokens_from_messages(messages_dict))

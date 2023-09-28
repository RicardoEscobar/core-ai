"""Gets the amount of tokens from a str"""
import tiktoken

def get_token_count(text: str, gpt_model: str = "gpt-4") -> int:
        """Return the number of tokens given a text and a GPT model"""

        # To get the tokeniser corresponding to a specific model in the OpenAI API:
        encoding = tiktoken.encoding_for_model(gpt_model)

        # Encode a string into tokens
        tokens = encoding.encode(text)

        # Count the number of tokens
        num_tokens = len(tokens)

        return num_tokens
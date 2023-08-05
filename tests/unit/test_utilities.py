"""Unit tests for the utilities module."""
# add the project root directory to the system path
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent.parent
    print(project_directory)
    import sys

    # sys.path.insert(0, str(project_directory))
    sys.path.append(str(project_directory))
    print(sys.path)

import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from unittest.mock import call
from unittest.mock import ANY

from controller.utilities import chat_completion_request
from controller.utilities import pretty_print_conversation

from controller.create_logger import create_logger

module_logger = create_logger(
    logger_name="tests.unit.test_utilities",
    logger_filename="test_utilities.log",
    log_directory="logs",
    add_date_to_filename=False,
)


class TestUtilities(unittest.TestCase):
    """Test the utilities module."""

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.logger = module_logger

    def setUp(self) -> None:
        """Run before each test."""
        self.functions = [
            {
                "name": "get_current_weather",
                "description": "Get the current weather",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "format": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "The temperature unit to use. Infer this from the users location.",
                        },
                    },
                    "required": ["location", "format"],
                },
            },
            {
                "name": "get_n_day_weather_forecast",
                "description": "Get an N-day weather forecast",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "format": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "The temperature unit to use. Infer this from the users location.",
                        },
                        "num_days": {
                            "type": "integer",
                            "description": "The number of days to forecast",
                        },
                    },
                    "required": ["location", "format", "num_days"],
                },
            },
        ]

    def tearDown(self) -> None:
        """Run after each test."""
        self.functions = None

    def test_chat_completion_request(self):
        """Test the chat_completion_request function."""

        # Mock the requests.post function
        mock_post = MagicMock()
        mock_post.return_value = "mock response"
        with patch("controller.utilities.requests.post", mock_post):
            # Test the function
            response = chat_completion_request(
                messages=[{"role": "user", "content": "Hello!"}]
            )

        # Verify the response
        self.assertEqual(response, "mock response")
        self.logger.debug("response: %s", response)

        # Verify the call to requests.post
        mock_post.assert_called_once_with(
            "https://api.openai.com/v1/chat/completions",
            headers=ANY,
            json={
                "model": "gpt-3.5-turbo-0613",
                "messages": [{"role": "user", "content": "Hello!"}],
            },
            timeout=10,
        )
        self.logger.debug("mock_post.call_args_list: %s", mock_post.call_args_list)

    def test_pretty_print_conversation(self):
        """Test the pretty_print_conversation function."""

        # Mock the print function
        mock_print = MagicMock()
        with patch("controller.utilities.print", mock_print):
            # Test the function
            pretty_print_conversation(
                messages=[
                    {"role": "user", "content": "Hello!"},
                    {"role": "system", "content": "Hi!"},
                ]
            )

        # Verify the calls to print
        expected_calls = [
            call("\x1b[32muser: Hello!\n\x1b[0m"),
            call("\x1b[31msystem: Hi!\n\x1b[0m"),
        ]
        mock_print.assert_has_calls(expected_calls)
        self.logger.debug("mock_print.call_args_list: %s", mock_print.call_args_list)

        # Mock the print function
        mock_print = MagicMock()
        with patch("controller.utilities.print", mock_print):
            # Test the function
            pretty_print_conversation(messages=[])

        # Verify the calls to print with an empty list
        expected_calls = []
        mock_print.assert_has_calls(expected_calls)
        self.logger.debug("mock_print.call_args_list: %s", mock_print.call_args_list)

    @patch("controller.utilities.requests.post")
    def test_chat_completion_request_with_functions(self, mock_post: MagicMock):
        """Test the chat_completion_request function with functions."""
        # Mock the response from the OpenAI API
        mock_post.return_value = MagicMock()
        mock_post.return_value.json.return_value = {
            "choices": [
                {
                    "text": "Sure, I can help with that. Can you please provide me with your location?",
                    "index": 0,
                    "logprobs": None,
                    "finish_reason": "stop",
                    "length": 73,
                    "model": "gpt-3.5-turbo-0613",
                }
            ]
        }
        messages = []
        messages.append({"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
        messages.append({"role": "user", "content": "What's the weather like today"})
        self.logger.debug("messages =  %s", messages)

        chat_response = chat_completion_request(
            messages, functions=self.functions
        )
        assistant_message = chat_response.json()["choices"][0]["message"]
        messages.append(assistant_message)
        self.logger.debug("assistant_message =  %s", assistant_message)


if __name__ == "__main__":
    unittest.main()

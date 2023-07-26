import openai
import json

from controller.conversation.load_openai import load_openai
from controller.vrchat import VRChat

load_openai()


def dance():
    """Send the dance emote to the VRChat client, when assistant is asked to dance or to show a talent it has."""
    vrchat = VRChat()
    response = "Of course! look I'm Dancing!"
    # Send the greeting to the VRChat client.
    vrchat.send_text(response)
    # Send wave emote to the VRChat client.
    vrchat.send_vrc_emote("a1-dance")

    result = {
        "response": response,
    }

    return json.dumps(result)


# Example dummy function hard coded to return the hello world message.
def greet_user(
    greeting: str = "Hello world!",
):
    """Response to the user the greeting message when the user greets the assistant, if the user mentions his or her name, it uses it as part of the greeting message."""
    # Create VRChat client to send the greeting to the VRChat client.
    vrchat = VRChat()
    # Send the greeting to the VRChat client.
    vrchat.send_text(greeting)
    # Send wave emote to the VRChat client.
    vrchat.send_vrc_emote("wave")

    response = {
        "greeting": greeting,
    }
    print(f"response = {repr(response)}")

    return json.dumps(response)


# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)


def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    # messages = [{"role": "user", "content": "What's the weather like in Boston?"}]
    messages = [
        {
            "role": "system",
            "content": "You are connected to VRChat as an AI assistant. The user may ask you to do things in VRChat. You may dance, since now you control the avatar in VRChat. So answer like you would as if you did the action yourself. Your name is Ann, you may greet the user.",
        },
        {
            "role": "user",
            "content": "Hello there! My name is Ricardo. What's your name?",
        },
    ]
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
        {
            "name": "greet_user",
            "description": "Runs whenever the user greets the assistant, sends a `greeting` message to the VRChat client",
            "parameters": {
                "type": "object",
                "properties": {
                    "greeting": {
                        "type": "string",
                        "description": "The `greeting` message sent to the VRChat client",
                    },
                },
                "required": ["greeting"],
            },
        },
        {
            "name": "dance",
            "description": "Send the dance emote to the VRChat client, when assistant is asked to dance or to show a talent it has",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4-0613", # "gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]
    print(f"response_message = {repr(response_message)}")
    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        print("response_message.get('function_call') is True")
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_current_weather": get_current_weather,
            "greet_user": greet_user,
            "dance": dance,
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = fuction_to_call(**function_args)
        # function_response = fuction_to_call(
        #     location=function_args.get("location"),
        #     unit=function_args.get("unit"),
        # )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response

        second_response = openai.ChatCompletion.create(
            model="gpt-4-0613", # "gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        print(f"second_response = {repr(second_response)}")

        return second_response
    else:
        raise Exception("GPT-3 did not call a function")


print(run_conversation())

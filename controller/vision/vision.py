from openai import OpenAI
import base64


from controller.load_openai import load_openai
from controller.time_it import time_it

load_openai()

client = OpenAI()

@time_it
def vision_url():
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {
                        "type": "image_url",
                        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    return response

@time_it
def vision_file():
    # Path to your image
    image_path = "test2_empty_space.png"

    # Getting the base64 string
    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this picture in spanish."}, # "This is a VRChat avatar chattting with you, answer to it and compliment the avatar, describing a cute detail about it. Do it in Spanish."}, # "This is a VRChat avatar on this picture, if the name shows avobe it what is it? if there is a chat message, what does it say? and describe the avatar"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    return response

@time_it
# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

@time_it
def main():
    response = vision_file()
    print(response.choices[0])


if __name__ == "__main__":
    main()

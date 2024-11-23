from os import getenv
import logging

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=getenv("OPENROUTER_API_KEY"),
)


def openrouter_vlm(prompt: str, img_str: str) -> str:
    """
    Generates a response from the OpenRouter VLM model based on a given text prompt and image URL.
    """

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": img_str
                    }
                }
            ]
        }
    ]

    completion = client.chat.completions.create(
        model="meta-llama/llama-3.2-90b-vision-instruct:free",
        messages=messages,
        max_tokens=None,
    )
    response = completion.choices[0].message.content

    logging.debug(response)

    return response

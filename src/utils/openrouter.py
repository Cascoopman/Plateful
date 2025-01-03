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

def openrouter_llm(prompt: str, text: str) -> str:
    """
    Generates a response from an OpenRouter LLM model based on a given prompt and text.
    """
    AVAILABLE_FREE_LLMS = [
        "meta-llama/llama-3.1-70b-instruct:free",
        "nousresearch/hermes-3-llama-3.1-405b:free",
    ]

    completion = None
    for model in AVAILABLE_FREE_LLMS:
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text}
                ]
            )
            if completion and completion.choices:
                break
        except Exception as e:
            logging.error(f"Limit reached of model {model}: {e}")

    if not completion or not completion.choices:
        logging.error("All models are exhausted.")
        return ""

    logging.debug(completion.choices[0].message.content)

    return completion.choices[0].message.content

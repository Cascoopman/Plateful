from openai import OpenAI
from os import getenv
import os
from dotenv import load_dotenv
import base64

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=getenv("OPENROUTER_API_KEY"),
)

file_name = "menu_image_pizza.jpg"
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

with open(file_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

img_str = f"data:image/jpeg;base64,{encoded_image}"

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": """Extract all the food items from the given menu. 
                For each item, list the dish name followed by its ingredients in parentheses. 
                Format each item on a new line like this: 'Dish Name (ingredient1, ingredient2, ingredient3)'
                Only include dishes with their ingredients in parentheses, and exclude any additional information such as prices or descriptions that are not part of the dish or its ingredients.
                Do not include additional explanations or text.
                If there are no food items or menu, output test
                """
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
    max_tokens=300
)

output_text = completion.choices[0].message.content

with open("menu_to_text.txt", "w") as file:
    file.write(output_text)
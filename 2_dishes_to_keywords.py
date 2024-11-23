import os
from os import getenv
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=getenv("OPENROUTER_API_KEY"),
)

def process_line(line, output_file, is_last_line):
    prompt = f"""
    Given a dish name and its ingredients, find at most 3 keywords to find the most relevant picture of that dish.
    Ensure good SEO, such that the first image returned gives a very clear idea of the dish.
    Output the keywords in one line separated by spaces.
    Do not use any other delimiters.
    Do not output any explanation or other output aside from the keywords.
    In English.
    """
    response = get_llm_response(prompt, line)
    print(response)
    with open(output_file, 'a') as file:
        if is_last_line:
            file.write(response)
        else:
            file.write(response + '\n')

def read_and_process_file(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                is_last_line = (i == len(lines) - 1)
                process_line(line, output_file_path, is_last_line)
    except FileNotFoundError:
        print(f"The file {input_file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_llm_response(prompt, text):
    completion = client.chat.completions.create(
        model="meta-llama/llama-3.1-70b-instruct:free",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
    )
    if completion and completion.choices:
        return completion.choices[0].message.content
    else:
        print("No completion returned.")
        return ""

if __name__ == "__main__":
    input_file_path = os.path.join(os.path.dirname(__file__), 'menu_to_text.txt')
    output_file_path = os.path.join(os.path.dirname(__file__), 'text_to_keywords.txt')
    read_and_process_file(input_file_path, output_file_path)
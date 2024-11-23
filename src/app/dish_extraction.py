"""This module provides functionality to extract dish information from a menu image."""

import base64
import os
import json
import logging

from src.models.menu import Menu, Dish
from utils.openrouter import openrouter_vlm

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)


def read_image_to_str(file_name: str) -> str:
    """
    Read an image from the menu_pictures folder into a base64 format
    """

    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../../menu_pictures", file_name
    )

    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    return f"data:image/jpeg;base64,{encoded_image}"


def get_extraction_prompt() -> str:
    """
    Return the prompt to instruct a model to extract the dishes
    """
    return """
        You are a helpful assistant that outputs a JSON.

        *Task*
        Your task is to extract all the dishes from a given menu image.
        For each item, list the dish name followed by its ingredients in parentheses.

        *Dish*
        A dish is an item on the menu that is considered a standalone item.
        It has a name, often a price, sometimes ingredients, and maybe a description.
        It is not comprised of sub-dishes nor is it a supplement or add-on.
        Examples of dishes: drinks, desserts, main courses, etc.
        Examples of non-dishes: sauces, menu (sub)titles, etc.

        *Format*
        You must output all the dishes in a dictionary.
        Use the following output format:
        [FORMAT]
        {
            "dish_1": {
                "name": str,
                "ingredients": list[str] (optional),
                "price": int (optional),
                "description": str (optional)
            },
            "dish_2": {
                ...
            }
        }
        [/FORMAT]
        If one of the fields is not mentioned on the menu, do not return any value for it.
        Do not output an explanation, additional text, or extra formatting.
        If the image does not contain dishes, output a single dish with the name "ERROR".
    """


def extract_json_from_response(output: str) -> dict:
    """
    Extract the JSON part from the LLM or VLM output
    """

    json_start = output.find("{")
    json_end = output.rfind("}") + 1

    json_content = output[json_start:json_end]

    logging.debug(json_content)

    try:
        dishes_dict = json.loads(json_content)
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from the output")

    if dishes_dict.get("ERROR"):
        logging.error("Not able to identify a menu or dishes.")

    return dishes_dict


def dishes_dict_to_menu(dishes_dict) -> Menu:
    """
    This function converts a dictionary of dishes to a list of Dish objects
    """
    dishes_list = []
    for name, values in dishes_dict.items():
        dish = Dish(
            name=name,
            ingredients=values.get("ingredients"),
            price=values.get("price"),
            description=values.get("description")
        )
        dishes_list.append(dish)
    return Menu(dishes_list)


def extract_menu_from_image(file_name: str) -> Menu:
    """
    This function takes a picture of a menu and extracts dishes.
    Dishes are the items that can be bought and usually have a name, ingredients
    """
    img_str = read_image_to_str(file_name)

    prompt = get_extraction_prompt()

    response = openrouter_vlm(prompt, img_str)

    dishes_dict = extract_json_from_response(response)

    return dishes_dict_to_menu(dishes_dict)


if __name__ == "__main__":

    FILE_NAME = "menu_image_pizza.jpg"

    menu = extract_menu_from_image(FILE_NAME)

    logging.info(menu)

"""This module provides functionality to search images for the dishes."""

import logging

from src.models.menu import Menu
from utils.openrouter import openrouter_llm
from utils.google_api import google_img_search


logging.basicConfig(level=logging.DEBUG)


def get_keyword_prompt(max_keywords: int = 3) -> str:
    """
    This function returns the prompt for instructing an LLM to generate keywords.
    """

    return f"""
    You are an AI assistant.

    *Task*
    Generate up to {max_keywords} keywords for searching an image of a dish.
    Use the dish name, ingredients, price, and description if available.
    Ensure the keywords optimize SEO for clear identification of the dish.

    *Format*
    Provide the keywords in a single line, separated by spaces.
    Only output the keywords, nothing else.
    """


def set_keywords(menu: Menu, max_keywords: int = 3) -> None:
    """
    This function sets the search keywords for each dish in the menu
    """
    for dish in menu.dishes:
        prompt = get_keyword_prompt(max_keywords)

        dish_text = str(dish)

        dish.keywords = openrouter_llm(prompt, dish_text)


def retrieve_images(menu: Menu) -> None:
    """
    This function uses the dish keywords to retrieve an google image url
    """
    for dish in menu.dishes:
        dish.image_url = google_img_search(query=dish.keywords)


if __name__ == "__main__":
    import pickle

    with open('tests/test_menu.pkl', 'rb') as f:
        test_menu = pickle.load(f)

    set_keywords(test_menu)

    retrieve_images(test_menu)

    logging.debug(test_menu)

    with open('tests/test_menu.pkl', 'wb') as f:
        pickle.dump(test_menu, f)

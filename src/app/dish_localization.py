"""This module provides functionality to locate the dishes on the menu image."""

import logging
import pickle

import easyocr
import cv2
from fuzzywuzzy import process

from utils.ocrspace import OcrClient
from models.menu import Menu

logging.basicConfig(level=logging.DEBUG)


def format_easy_ocr(results):
    """
    This function ensures the local output matches the output from the API
    """
    formatted_results = []

    for (bbox, text, _) in results:
        top_left, _, bottom_right, _ = bbox
        formatted_results.append({
            "LineText": text,
            "Words": [{
                "Top": int(top_left[1]),
                "Left": int(top_left[0]),
                "Height": int(bottom_right[1] - top_left[1]),
                "Width": int(bottom_right[0] - top_left[0])
            }]
        })

    logging.debug(formatted_results)

    return formatted_results


def perform_local_ocr(menu: Menu):
    """
    This function recognizes and locates the text in the menu picture
    """
    reader = easyocr.Reader(['en', 'fr', 'es', 'de', 'it', 'nl'])

    image = cv2.imread(menu.image_path)

    results = reader.readtext(image)

    return format_easy_ocr(results)


def perform_cloud_ocr(menu: Menu) -> list[dict]:
    """
    This function makes a request to the ocrspace API for ocr as a service
    """
    return OcrClient().ocr_file(menu.image_path)


def locate_dishes_in_menu(menu: Menu, identified_lines):
    """
    This function links the ocr text localization to the menu's dishes
    """
    for dish in menu.dishes:
        best_match = process.extractOne(
            dish.name,
            [line_text.get('LineText') for line_text in identified_lines]
            )

        if best_match:
            word = best_match[0]

            menu.dish_locations[dish.id]["identified_line_text"] = word

            for line in identified_lines:
                if line["LineText"] == word:
                    location_info = line["Words"][0]
                    location = (location_info["Top"], location_info["Left"])
                    menu.dish_locations[dish.id]["location"] = location
                    break


if __name__ == "__main__":
    with open('/Users/cas/Projects/Plateful/tests/test_menu.pkl', 'rb') as file:
        test_menu = pickle.load(file)

    extracted_lines = perform_local_ocr(test_menu)
    #extracted_lines = perform_cloud_ocr(test_menu)

    locate_dishes_in_menu(test_menu, extracted_lines)

    with open('/Users/cas/Projects/Plateful/tests/test_menu.pkl', 'wb') as file:
        pickle.dump(test_menu, file)

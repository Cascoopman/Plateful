import sys
import os
import logging

import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("CUSTOM_SEARCH_API")
cx = os.getenv("CX")
SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

if not api_key or not cx:
    logging.error("API key or CX value missing. Please check your .env file.")
    sys.exit()

def google_img_search(query: str, number_of_images: int = 1) -> str:
    """
    This function retrieves a number of images from google based on the input query
    """

    params = {
        "q": query,
        "cx": cx,
        "key": api_key,
        "searchType": "image",
        "num": number_of_images
    }

    try:
        response = requests.get(SEARCH_URL, params=params, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        search_results = response.json()

        if "items" in search_results:
            return search_results["items"][0]["link"]

        logging.debug(
            "Not a single image found through google image search api. (query: %s)",
            query
            )

        return None

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving image for '{query}': {e}")
        return None

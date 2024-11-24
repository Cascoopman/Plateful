import pickle
import logging

from app.dish_extraction import extract_menu_from_image
from app.image_retrieval import set_keywords, retrieve_images
from app.dish_localization import perform_local_ocr, perform_cloud_ocr, locate_dishes_in_menu
from utils.helpers import save_menu


def main(file_name: str) -> None:
    """
    This function goes through the entire plateful logic
    """

    menu = extract_menu_from_image(file_name)

    save_menu(menu, f"output/{file_name}.pkl")
    logging.debug(menu)
    
    set_keywords(menu)

    retrieve_images(menu)

    save_menu(menu, f"output/{file_name}.pkl")
    logging.debug(menu)

    extracted_lines = perform_cloud_ocr(menu)
    #extracted_lines = perform_local_ocr(menu)

    locate_dishes_in_menu(menu, extracted_lines)
    save_menu(menu, f"output/{file_name}.pkl")
    logging.debug(menu)

if __name__ == "__main__":
    MENU_NAME = 'kanun_thai'
    main(MENU_NAME)

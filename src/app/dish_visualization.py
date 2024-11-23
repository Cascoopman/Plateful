"""This module provides functionality to visualize all the dishes."""

import logging
import pickle

from reportlab.pdfgen import canvas as cv
from reportlab.lib.utils import ImageReader

from models.menu import Menu

logging.basicConfig(level=logging.DEBUG)


def create_clickable_pdf(menu: Menu, output_pdf_path: str):
    """
    This function creates a new pdf file from scratch
    by first reading in the menu image from the menu.image_path
    and putting it as background image.
    Second it places clickable buttons on each dish in 
    menu.dish_locations and uses menu.dish_locations[dish.id]["location"]
    tuple containing (x, y) coordinates.
    """
    # Initialize the canvas for the PDF
    pdf_canvas = cv.Canvas(output_pdf_path)

    # Draw the menu image as the background
    menu_image = ImageReader(menu.image_path)
    image_width, image_height = menu_image.getSize()
    pdf_page_width = pdf_canvas._pagesize[0]
    pdf_page_height = pdf_canvas._pagesize[1]
    pdf_canvas.drawImage(menu_image, 0, 0, width=pdf_page_width, height=pdf_page_height)

    # Calculate the scaling factors
    x_scale = pdf_page_width / image_width
    y_scale = pdf_page_height / image_height

    # Add clickable buttons for each dish
    button_size = 15  # Size of the clickable rectangle
    for dish_id, location in menu.dish_locations.items():
        y, x = location["location"]  # Coordinates for the dish
        dish = menu.get_dish_by_id(dish_id)  # Get dish details

        # Scale the coordinates
        scaled_x = x * x_scale
        scaled_y = pdf_page_height - (y * y_scale) - button_size

        # Draw a transparent clickable rectangle
        pdf_canvas.setFillColorRGB(1, 0, 0, alpha=0.5)  # Semi-transparent red fill
        pdf_canvas.setStrokeColorRGB(1, 0, 0)  # Red border
        pdf_canvas.rect(scaled_x, scaled_y, button_size, button_size, fill=1, stroke=1)

        # Add a hyperlink to the rectangle
        pdf_canvas.linkURL(dish.image_url,
                           (scaled_x, scaled_y, scaled_x + button_size, scaled_y + button_size),
                           relative=1)

    # Save the PDF
    pdf_canvas.save()


if __name__ == "__main__":
    with open('/Users/cas/Projects/Plateful/tests/test_menu.pkl', 'rb') as file:
        test_menu = pickle.load(file)

    create_clickable_pdf(test_menu, "output/test_menu.pdf")
    #add_clickable_links(test_menu)

    with open('/Users/cas/Projects/Plateful/tests/test_menu.pkl', 'wb') as file:
        pickle.dump(test_menu, file)

import os

from flask import Flask, jsonify, render_template, request, send_from_directory

from models.menu import Menu
from utils.helpers import load_menu

app = Flask(__name__)

# Load the menu from the file
MENU_PATH = 'tests/test_menu.pkl'
menu = load_menu(MENU_PATH) if os.path.exists(MENU_PATH) else None

@app.route("/")
def index():
    """
    Render the main page with the menu image.
    """
    if not menu:
        return "Menu file not found. Please check the path.", 500
    print(menu)
    return render_template("index.html", dish_locations=menu.dish_locations, image_url="/static/test_menu.jpg")


@app.route("/get_dish/<dish_id>")
def get_dish(dish_id):
    """
    Fetch dish details based on dish ID.
    """
    if not menu:
        return jsonify({"error": "Menu not loaded"}), 500
    print(type(dish_id))
    dish = menu.get_dish_by_id(dish_id)
    if not dish:
        return jsonify({"error": "Dish not found"}), 404

    return jsonify({
        "name": dish.name,
        "image_url": dish.image_url,
        "description": dish.description
    })


@app.route("/static/<path:path>")
def static_files(path):
    """
    Serve static files such as images.
    """
    return send_from_directory("static", path)


if __name__ == "__main__":
    app.run(debug=True)

import uuid

class Dish():
    """
    This dataclass represents a dish that was extracted from a menu.
    """

    def __init__(self, **kwargs):
        self.id = uuid.uuid4()
        self.name = kwargs.get('name', None)
        self.ingredients = kwargs.get('ingredients', [])
        self.price = kwargs.get('price', 0.0)
        self.description = kwargs.get('description', None)
        self.keywords = kwargs.get('keywords', None)
        self.image_url = kwargs.get('image_url', None)

    def __str__(self):
        ingredients = ', '.join(self.ingredients) if self.ingredients else 'None'
        price_str = f"${self.price:.2f}" if self.price is not None else 'None'

        return (
            f"Dish {self.id}:\n"
            f"  Name: {self.name or 'None'}\n"
            f"  Ingredients: {ingredients}\n"
            f"  Price: {price_str}\n"
            f"  Description: {self.description or 'None'}\n"
            f"  Keywords: {self.keywords or 'None'}\n"
            f"  Image URL: {self.image_url or 'None'}\n"
        )

class Menu():
    """
    This class represents a menu containing multiple dishes.
    """
    def __init__(self, name=None, dishes=None):
        self.name = name

        if name is not None:
            self.image_path = "menu_pictures/" + self.name + ".jpg"
            self.clickable_pdf_path = "output/dynamic_" + self.name + ".pdf"

        if dishes is None:
            self.dishes = []
        else:
            for dish in dishes:
                self.add_dish(dish)

        self.dish_locations = {}

    def __str__(self):
        menu_str = (
            "-"*75 + "\n"
            f"Menu extracted from {self.image_path}:\n"
            + "-"*75 + "\n\n"
        )

        menu_str += "Menu dishes\n------------\n"
        for dish in self.dishes:
            menu_str += str(dish) + "\n"

        menu_str += "Dish locations\n--------------\n"
        for dish_id, location_info in self.dish_locations.items():
            menu_str += (
            f"    Dish Name: {self.get_dish_by_id(dish_id).name}\n"
            f"    Identified Line Text: {location_info['identified_line_text'] or 'None'}\n"
            f"    Location: {location_info['location'] or 'None'}\n\n"
            )

        return menu_str

    def __iter__(self):
        return iter(self.dishes)

    def add_dish(self, dish, location=None, identified_line_text=None):
        self.dishes.append(dish)
        self.dish_locations[dish.id] = {
            "identified_line_text": identified_line_text,
            "location": location
        }

    def remove_dish(self, dish_id):
        self.dishes = [dish for dish in self.dishes if dish.id != dish_id]
        if dish_id in self.dish_locations:
            del self.dish_locations[dish_id]

    def get_dish_by_id(self, dish_id):
        for dish in self.dishes:
            if dish.id == dish_id:
                return dish
        return None

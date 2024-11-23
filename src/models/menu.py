class Dish():
    """
    This dataclass represents a dish that was extracted from a menu.
    """
    def __init__(self, **kwargs):
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
            f"Dish:\n"
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
    def __init__(self, dishes=None):
        if dishes is None:
            dishes = []
        self.dishes = dishes

    def add_dish(self, dish):
        if isinstance(dish, Dish):
            self.dishes.append(dish)
        else:
            raise TypeError("Only Dish instances can be added to the menu")

    def __str__(self):
        menu_str = "Menu:\n"
        for dish in self.dishes:
            menu_str += str(dish) + "\n"
        return menu_str

    def __iter__(self):
        return iter(self.dishes)

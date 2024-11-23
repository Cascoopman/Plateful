class Dish():
    """
    This dataclass represents a dish that was extracted from a menu.
    """
    def __init__(self, name=None, ingredients=None, price=None, description=None):
        self.name = name
        self.ingredients = ingredients if ingredients is not None else []
        self.price = price if price is not None else 0.0
        self.description = description

    def __str__(self):
        ingredients = ', '.join(self.ingredients)
        return f"Dish:\nName: {self.name}\nIngredients: {ingredients}\nPrice: ${self.price:.2f}\n"

from src.app.dish_extraction import dishes_dict_to_menu

FILE_NAME = "menu_image_pizza"

TEST_MENU_JSON = {
    "Fatto Tiramisu": {
        "name": "Fatto Tiramisu",
        "ingredients": ["Coffee liqueur soaked sponge", "mascarpone", "chocolate"],
        "price": 7
    },
    "Scugnizielli Nutella & Gelato": {
        "name": "Scugnizielli Nutella & Gelato",
        "ingredients": ["Fried mini pizza doughnuts", "Nutella", "vanilla gelato"],
        "price": 7.5
    },
    "Affogato": {
        "name": "Affogato",
        "ingredients": ["Vanilla gelato", "espresso"],
        "price": 6
    },
    "Affogato Limoncello": {
        "name": "Affogato Limoncello",
        "ingredients": ["Lemon sorbet", "limoncello"],
        "price": 7.5
    },
    "Gelato Sandwich": {
        "name": "Gelato Sandwich"
    },
    "Lemon Meringue": {
        "name": "Lemon Meringue",
        "ingredients": ["Vanilla biscuit filled with vanilla gelato", "lemon curd & meringue"],
        "price": 7
    },
    "Chocolate Salted Caramel": {
        "name": "Chocolate Salted Caramel",
        "ingredients": ["Chocolate dipped biscuit filled with salted caramel gelato"],
        "price": 7
    },
    "Chocolate Orange": {
        "name": "Chocolate Orange",
        "ingredients": ["Chocolate biscuit filled with chocolate orange gelato"],
        "price": 7
    },
    "Digestivo": {
        "name": "Digestivo"
    },
    "Coffee": {
        "name": "Coffee"
    }
}

TEST_MENU = dishes_dict_to_menu(FILE_NAME, TEST_MENU_JSON)

import pickle

from models.menu import Menu

def load_menu(file_path: str) -> Menu:
    """
    Load the menu object from a pickle file.
    """
    with open(file_path, 'rb') as file:
        return pickle.load(file)


def save_menu(menu: Menu, file_path: str) -> None:
    """
    Save the menu object to a pickle file.
    """
    with open(file_path, 'wb') as file:
        pickle.dump(menu, file)

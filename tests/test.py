import pickle

from test_menu import TEST_MENU

print(TEST_MENU)

with open('/Users/cas/Projects/Plateful/tests/test_menu.pkl', 'rb') as file:
    test_menu = pickle.load(file)

print(test_menu)

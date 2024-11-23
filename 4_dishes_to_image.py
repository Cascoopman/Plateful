import easyocr
import cv2
from fuzzywuzzy import process
from matplotlib.backend_bases import MouseButton
import webbrowser
webbrowser.register('safari', None, webbrowser.MacOSXOSAScript('safari'))
import matplotlib.pyplot as plt

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

# Path to the image
image_path = '/Users/cas/Projects/Plateful/menu_image_pizza.jpg'

# Read the image
image = cv2.imread(image_path)

# Perform OCR on the image
results = reader.readtext(image_path)

print(results)

# Load the dishes from the menu_to_text.txt file
with open('/Users/cas/Projects/Plateful/menu_to_text.txt', 'r') as file:
    dishes = [line.split('(')[0].strip() for line in file.readlines()]

# Extract the text from the OCR results
extracted_texts = [text for (_, text, _) in results]

# Match each dish with the most relevant bounding box
matched_dishes = {}
for dish in dishes:
    best_match = process.extractOne(dish, extracted_texts)
    if best_match:
        matched_dishes[dish] = best_match

import matplotlib.patches as patches

# Load the URLs from the image_urls.txt file
with open('/Users/cas/Projects/Plateful/only_urls.txt', 'r') as file:
    urls = [line.strip() for line in file.readlines()]

# Create a dictionary to map dishes to URLs
dish_to_url = dict(zip(dishes, urls))

# Function to handle mouse clicks
def on_click(event):
    if event.button is MouseButton.LEFT:
        for dish, (matched_text, _) in matched_dishes.items():
            for (bbox, text, _) in results:
                if text == matched_text:
                    (top_left, _, bottom_right, _) = bbox
                    if top_left[0] <= event.xdata <= bottom_right[0] and top_left[1] <= event.ydata <= bottom_right[1]:
                        url = dish_to_url.get(dish)
                        if url:
                            print(f'Opening URL for {dish}: {url}')
                            webbrowser.get('safari').open(url)

# Connect the click event to the handler
fig, ax = plt.subplots()
ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
fig.canvas.mpl_connect('button_press_event', on_click)

# Draw the bounding boxes and texts
for dish, (matched_text, score) in matched_dishes.items():
    for (bbox, text, prob) in results:
        if text == matched_text:
            (top_left, top_right, bottom_right, bottom_left) = bbox
            rect = patches.Rectangle(top_left, bottom_right[0] - top_left[0], bottom_right[1] - top_left[1], linewidth=2, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
            ax.text(top_left[0], top_left[1] - 10, text, fontsize=12, color='red', weight='bold')

plt.axis('off')
plt.show()
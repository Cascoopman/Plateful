import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Retrieve API Key and CX from environment variables
api_key = os.getenv("CUSTOM_SEARCH_API")
cx = os.getenv("CX")

# Function to get the image URL from Google Custom Search API
def get_image_url(api_key, cx, query):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "cx": cx,
        "key": api_key,
        "searchType": "image",
        "num": 1
    }
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        search_results = response.json()
        
        if "items" in search_results:
            return search_results["items"][0]["link"]
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving image for '{query}': {e}")
        return None

# Main program logic
if __name__ == "__main__":
    # Ensure API key and CX values are present
    if not api_key or not cx:
        print("API key or CX value missing. Please check your .env file.")
        exit(1)

    # Open and read queries from the file
    try:
        with open("text_to_keywords.txt", "r") as file:
            queries = file.readlines()
        
        # Open the output file to store URLs
        with open("image_urls.txt", "w") as output_file:
            # Process each query
            for query in queries:
                query = query.strip()
                if not query:  # Skip if the query is empty
                    continue
                image_url = get_image_url(api_key, cx, query)
                if image_url:
                    output_file.write(f"{query}: {image_url}\n")
                    print(f"Image URL for '{query}': {image_url}")
                else:
                    output_file.write(f"{query}: No image found\n")
                    print(f"No image found for '{query}'")
                print("-" * 40)  # Separator for clarity between results
    except FileNotFoundError:
        print("The file 'text_to_keywords.txt' was not found.")

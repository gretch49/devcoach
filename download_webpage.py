import os
import requests
from html2markdown import convert
from bs4 import BeautifulSoup

# Retrieve API key from environmental variable
API_KEY = os.getenv("OPENAI_API_KEY")

def download_webpage(url):
    try:
        # Send a GET request to the URL to fetch the webpage content
        headers = {'Content-Type': 'text/html; charset=utf-8'}  # Add headers to specify encoding
        response = requests.get(url.encode('utf-8'), headers=headers)  # Encode the URL using UTF-8
        
        response.raise_for_status()  # Raise an exception for any HTTP errors

        # Parse the HTML content of the webpage using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the text content from the webpage
        text_content = soup.get_text()

        return text_content
    except requests.exceptions.RequestException as e:
        print(f"Failed to download webpage from {url}: {e}")
        return None

def save_content_to_file(content, url):
    # Extract filename from the URL
    filename = url.replace("https://", "")  # Remove the prefix
    filename = filename.strip("/")  # Remove leading/trailing slashes
    filename = filename.replace("/", "_")  # Replace remaining slashes with underscores

    # Convert HTML content to Markdown
    markdown_content = convert(content)

    # Ensure that the "data" folder exists within the project directory
    current_dir = os.path.dirname(__file__)
    data_folder = os.path.join(current_dir, "data")
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Write the content to a Markdown file in the "data" folder
    filepath = os.path.join(data_folder, f"{filename}.md")
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(markdown_content)

    print(f"Content saved to {filepath}")

# Example usage: Save webpage content to a Markdown file
    
while True:
    url = input('Type the URL of the page you want to add to the database. If you are done, type "done". \n\n URL or "done": ')
    if url == "done":
        print("Thanks, bye.")
        break
    else:
        webpage_content = download_webpage(url)
        if webpage_content:
            save_content_to_file(webpage_content, url)

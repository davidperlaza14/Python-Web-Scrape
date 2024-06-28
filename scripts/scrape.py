import requests 
import re
from bs4 import BeautifulSoup
import yaml
import logging
from scripts.utils import setup_logging, save_to_csv

def load_config(config_file):
    """
    Loads configuration from a YAML file.
    
    Args:
    config_file (str): Path to the configuration file.
    
    Returns:
    dict: Configuration loaded from the file.
    """
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

def fetch_page(url):
    """
    Fetches the content of the page.
    
    Args:
    url (str): URL of the webpage to request.
    
    Returns:
    bytes: Content of the webpage.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def parse_books(page_content):
    """
    Parses the content of the page to extract book information.
    
    Args:
    page_content (bytes): HTML content of the page.
    
    Returns:
    list of dict: List of dictionaries with book information.
    """
    soup = BeautifulSoup(page_content, 'html.parser')
    books = []
    for article in soup.find_all('article', class_='product_pod'):
        title = article.h3.a['title']
        price = article.find('p', class_='price_color').text
        price_cleaned = re.sub(r'[^\d.]', '', price)
        price_dollars = round(float(price_cleaned) * 1.3, 2)
        books.append({'title': title, 'price': price_dollars})
    return books 
    

def main():
    config = load_config('config.yaml')
    setup_logging(config['log_file'])

    all_books = []  
    for url in config['urls']:  
        logging.info(f"Fetching data from {url}")
        page_content = fetch_page(url)
        books = parse_books(page_content)  
        all_books.extend(books)

    save_to_csv(all_books, config['output_raw'])

if __name__ == "__main__":
    main() 

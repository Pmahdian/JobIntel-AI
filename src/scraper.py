import requests      
from bs4 import BeautifulSoup  
import pandas as pd 
import os           

def scrape_sample_data():
    """
    Scrape sample quotes from quotes.toscrape.com 
    This is for practice before moving to real job sites
    """
    try:
        print('Starting web scraper...')

        # URL for practice scraping
        url = 'https://quotes.toscrape.com'

        # Send GET request
        response = requests.get(url)
        print(f"Status codd: {response.status_code}")

        # check if the request was seuccessful
        if response.status_code == 200:
            # parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all quote elements
            quote_elements = soup.find_all('div', class_ =' quote')
            print(f"Found {len(quote_elements)} quotes")

            # Extract quote data
            quotes_data = []
            for quote in quote_elements:
                text = quote.find('span', class_ = 'text').text
                author = quote.find('small', class_ = 'author').text
                tags = [ tag.text for tag in quote.find_all('a', class_ = 'tag')]

                quotes_data.append({
                    'quote' : text,
                    'author' : author,
                    'tags' : tags
                })


            # Create data directpry if it dosen't exist
            os.makedirs('data', exist_ok= True)



    

    
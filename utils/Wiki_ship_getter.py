import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
from io import StringIO

def fetch_wikipedia_table(url,letter):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    for table in tables:
        caption = table.find('caption')
        if caption and caption.text.strip() == f'List of ships of World War II ({letter})':
            return table
    return None

def table_to_csv(table, output_path):
    table_html = str(table)
    df = pd.read_html(StringIO(table_html))[0]

    # Replace [NBSP] with a half-width space
    df.replace('\u00A0', ' ', regex=True, inplace=True)

    # Dictionary for navy name conversions
    navy_conversion = {
        'United States Navy': 'USA',
        'Royal Navy': 'ENG',
        'Imperial Japanese Navy': 'JPN',
        'Kriegsmarine': 'GER',
        'French Navy': 'FRA',
        'Chilean Navy': 'CHL',
        'destroyer': 'DD',
        'light cruiser': 'CL',
        'heavy cruiser': 'CA',
        'battleship': 'BB',
        'aircraft carrier': 'CV.txt',
        'submarine': 'SS',
        'minelayer': 'CM',
        'minesweeper': 'AM',
        'patrol boat': 'PB',
        'gunboat': 'GB',
        'sloop': 'SL',
        'corvette': 'K',
        'frigate': 'FF',
        'monitor': 'BM',
        'cruiser': 'C',
        'destroyer escort': 'DE',
        'escort destroyer': 'DE',
        'escort carrier': 'CVE',
        'landing ship': 'LST',
        'landing craft': 'LC',
        'landing craft tank': 'LCT',
        'super dreadnought': 'BB',
        'auxiliary cruiser': 'MC',
        'Protected cruiser': 'C',
        'landing ship, tank' : 'LST',
        'landing craft, infantry': 'LCI',
        'light aircraft carrier': 'CVL',
        'Sloop': 'SL',
        'minesweeper destroyer': 'DAM',
    }

    # Apply the conversions
    df.replace(navy_conversion, inplace=True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8')

if __name__ == "__main__":
    Alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    for letter in Alphabet:
        url = f'https://en.wikipedia.org/wiki/List_of_ships_of_World_War_II_({letter})'  # Example URL
        output_path = f'database/REAL_SHIP_DATA/ship_data_{letter}.csv'

        table = fetch_wikipedia_table(url,letter)
        if table:
            table_to_csv(table, output_path)
            print(f"CSV file has been created at {output_path}")
        else:
            print("No table found with the specified caption.")

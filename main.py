import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

# URL of the website to scrape
base_url = 'https://biosfera.kz/product/category?path=13&page='

# List to store extracted data
products = []

# number of attempts
max_attempts = 205

try:
    for attempt in range(1, max_attempts + 1):
        url = base_url + str(attempt)
        # Send an HTTP GET request to the website
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all <a> elements with a specific class name
        parent_tags = soup.find_all('div', class_='lotInfo')

        for tag in parent_tags:
            product_name = tag.find('div', class_='title').text.strip()
            product_price = tag.find('div', class_='priceLine').text.strip()
            products.append({
                'Name': product_name,
                'Price': product_price,
                'Date': datetime.now().strftime("%Y-%m-%d"),
                #'Time': datetime.now().strftime("%H:%M:%S")
                'Time': None  
            })

    if products:
        # Define CSV filename
        csv_filename = 'products.csv'

        # Check if the CSV file exists
        file_exists = os.path.isfile(csv_filename)

        # Write extracted data to CSV file
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Price', 'Date', 'Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write an empty row at the beginning of the file
            if file_exists:
                writer.writerow({})

            # Write headers if file doesn't exist
            if not file_exists:
                writer.writeheader()

            # Write data to the CSV file
            for product in products:
                writer.writerow(product)

        print(f"Extracted data written to {csv_filename}")
    else:
        print("No products found.")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

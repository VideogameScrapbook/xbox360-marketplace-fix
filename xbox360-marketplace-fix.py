# Bulk opens download links for Xbox 360 marketplace, getting around redirect error.
# To use, put links to https://marketplace.xbox.com/ pages in xbox360-marketplace-fix.txt

import requests
from bs4 import BeautifulSoup
import re
import webbrowser

def open_download_links(filename):
    try:
        with open(filename, 'r') as file:
            links = [line.strip() for line in file]

        # Process each link
        for url in links:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            download_links = soup.find_all('a', attrs={'role': 'button', 'data-purchaseurl': re.compile(r'https://live.xbox.com/en-US/purchase/xbox/[^"]+')})
            for link in download_links:
                download_url = link['data-purchaseurl']
                webbrowser.open_new_tab(download_url)
                print(f"Opened: {download_url}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    filename = "xbox360-marketplace-fix.txt"
    open_download_links(filename)

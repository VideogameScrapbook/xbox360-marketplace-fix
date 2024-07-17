# Bulk opens download links for Xbox 360 marketplace, getting around redirect error.
# This script prompts you for pages to search.
# Alternatively, you can put links to marketplace.xbox.com pages (or links to pages that have links) in xbox360-marketplace-fix.txt
# Each link in xbox360-marketplace-fix.txt should have its own separate line.

import os
import requests
from bs4 import BeautifulSoup
import re
import webbrowser

# Configurable variables:
open_download_links = True
only_free = False
download_link_limit = 30

# Optional prompts.
#open_download_links = input("Open found download links? (y/n): ").lower() == 'y'
#if open_download_links:
    #only_free = input("Open only free items? (y/n): ").lower() == 'y'

# Init variables:
download_links_opened = 0

def extract_purchase_urls(input_source):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the script directory
        if input_source and not os.path.isabs(input_source):
            input_source = os.path.join(script_dir, input_source)  # Make input_source relative to script_dir
            
        if os.path.exists(input_source):  # Check if it's a file
            with open(input_source, 'r') as file:
                links = [line.strip('\'"').strip() for line in file]  # Remove both leading and trailing quotes
        else:  # Assume it's a URL
            links = [input_source]
        
        #print(links)        
        
        # Process each link
        for url in links:                        
            # If link is to marketplace.xbox.com, start processing it for download urls.
            if "marketplace.xbox.com" in url:
                print(f"Adding {url} to the list of marketplace links to process.")
                open_download_urls(url)
            # Else, if link is to a different site, search it for marketplace links.
            else:
                response = requests.get(url)
                if response.status_code == 404:  # Check if the page exists
                    print(f"Page not found (HTTP {response.status_code}): {url}")
                else:
                    print(f"Looking for marketplace.xbox.com links on this page: {url}")
                    soup = BeautifulSoup(response.content, 'html.parser')
                    #print(response.content)
                    marketplace_links_on_page = soup.find_all('a', href=re.compile(r'https?://marketplace\.xbox\.com/[^"]+'))
                    #print(marketplace_links_on_page)
                    
                    # If using FREE XboxLoot.com page link as reference, remove first link on page which is to the whole listing.
                    if "freexboxloot.com" in url:
                        marketplace_links_on_page = marketplace_links_on_page[1:]
                        
                    open_download_urls([link['href'] for link in marketplace_links_on_page])


    except Exception as e:
        print(f"Error: {e}")

def open_download_urls(marketplace_links):
    # Process the expanded list of links
    for marketplace_url in marketplace_links:
        print(f"Looking for live.xbox.com links on the following page: {marketplace_url}")
        response_expanded = requests.get(marketplace_url)
        soup_expanded = BeautifulSoup(response_expanded.content, 'html.parser')
        
        if response_expanded.status_code == 404:  # Check if the page exists
            print(f"Page not found (HTTP {response_expanded.status_code}): {marketplace_url}")
        else:
            if open_download_links:
                download_links = soup_expanded.find_all('a', attrs={'role': 'button', 'data-purchaseurl': re.compile(r'https?://live.xbox.com/[^"]+/purchase/xbox/[^"]+')})
                for download_link in download_links:
                    download_url = download_link['data-purchaseurl']
                    span_before_link = download_link.find_previous_sibling('span')
                    if span_before_link:
                        is_free = "Free" in span_before_link.text
                        if not only_free or is_free:
                            response_download = requests.get(download_url)
                            soup_downloaded = BeautifulSoup(response_download.content, 'html.parser')
                            if response_download.status_code == 404:  # Check if the page exists
                                print(f"Page not found (HTTP {response_download.status_code}): {download_url}")
                            else:
                                webbrowser.open_new_tab(download_url)
                                print(f"Opened: {download_url}")
            else:
                webbrowser.open_new_tab(marketplace_url)
                print(f"Opened: {marketplace_url}")
                
                download_links_opened += 1
                
                if download_links_opened >= download_link_limit:
                    print(f"Download limit of {download_link_limit} has been reached, quitting.")

default_input_source_filename = "xbox360-marketplace-fix.txt"
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the script directory
default_input_source_path = os.path.join(script_dir, default_input_source_filename)  # Make default_input_source_path relative to script_dir

# Check if xbox360-marketplace-fix.txt exists
if os.path.exists(default_input_source_path):
    filename = "xbox360-marketplace-fix.txt"
else:
    user_url = input("Enter a URL (marketplace.xbox.com or any other page): ")
    user_url = user_url.strip('"')  # Remove double quotes
    user_url = user_url.strip("'")  # Remove single quotes
    filename = None

# Call the function
extract_purchase_urls(filename)

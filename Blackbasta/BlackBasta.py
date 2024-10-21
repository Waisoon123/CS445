# Author - Dexter Lim
# Blackbasta Tor Browser Scrapper

# Import Libraries
import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from typing import Dict, List

# Configure Selenium to use the Tor browser


def configure_tor_browser():
    options = Options()
    options.headless = True
    # This path should point to tor browser executable
    options.binary_location = r'/Applications/Tor Browser.app/Contents/MacOS/firefox'
    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.socks', '127.0.0.1')
    profile.set_preference('network.proxy.socks_port', 9150)
    profile.set_preference('network.proxy.socks_remote_dns', True)
    profile.update_preferences()

    options.profile = profile
    return webdriver.Firefox(options=options)

# Function to scrape the main page


def scrape_main_page(driver, url):
    print(f"Navigating to URL: {url}")
    driver.get(url)
    list_cards = []

    try:
        WebDriverWait(driver, 90).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.card')))
        print("Page loaded successfully")
    except Exception as e:
        print(f"Error: {e}")
        print("Page source for debugging:")
        print(driver.page_source)
        return

    total_pages = 22
    
    for page_num in range(1, total_pages + 1):
        #Scrape current page
        print(f"Scraping page {page_num}...")
        
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all divs with the class 'card'
        cards = soup.find_all('div', class_="card")

        # Print the content of each card
        for card in cards:
            title = card.find('div', class_="title").text.strip()
            subpage_url = card.find('a')['href']
            print(f"Title: {title}", f"subpage_url: {subpage_url}")
            list_cards.append({"title": title, "subpage_url": subpage_url})
        
        # Click the next page button
        if page_num < total_pages:  # Don't try to click next on the last page
            try:
                # You can also target the specific page number button if necessary
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.next-page-btn'))
                )
                next_button.click()
                
                # Give the page time to load before scraping
                time.sleep(10)
                
                WebDriverWait(driver, 90).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.card')))
            except Exception as e:
                print(f"Error navigating to page {page_num + 1}: {e}")
                break
    return list_cards

def scrape_subpage(driver, subpage_url):
    print(f"Navigating to subpage URL: {subpage_url}")  # Debugging print statement
    driver.get(subpage_url)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.vuepress-markdown-body')))
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    description_text = ""
    appended_texts = set()

    content_div = soup.find('div', class_='vuepress-markdown-body')
    
    if content_div:
        # Loop through <p> tags to find the main content
        paragraphs = content_div.find_all('p')

        for paragraph in paragraphs:
            text = paragraph.get_text(strip=True)
            if text and text not in appended_texts:
                description_text += text + "\n"
                appended_texts.add(text)

        # Now loop through <em> tags and check if the text was already appended
        emphasized_elements = content_div.find_all('em')
        for em in emphasized_elements:
            em_text = em.get_text(strip=True)
            if em_text and em_text not in appended_texts:
                description_text += em_text + "\n"
                appended_texts.add(em_text)
    
    disclosed_links = []
    data_links_div = soup.find('div', class_='data-links')
    if data_links_div:
        a_tags = data_links_div.find_all('a')  # Find all <a> tags within the data-links div
        disclosed_links = [a['href'] for a in a_tags if a.has_attr('href')]  # Extract href attribute

    return description_text, disclosed_links

def save_to_csv(data, filename):
    if not data:
        print("No data to save.")
        return

    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

# Example usage
if __name__ == "__main__":
    driver = configure_tor_browser()
    try:
        cards = scrape_main_page(driver, "http://stniiomyjliimcgkvdszvgen3eaaoz55hreqqx6o77yvmpwt7gklffqd.onion/")
        if not cards:
            print("No cards found.")
        results = []

        for card in cards:
            subpage_url = card['subpage_url']
            description, disclosed_links = scrape_subpage(driver, subpage_url)
            results.append({
                "Name": card['title'],
                "Description": description,
                "Disclosed Links": ", ".join(disclosed_links)
            })
        save_to_csv(results, 'scraped_data.csv')
    finally:
        driver.quit()

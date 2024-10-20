# Author - Lem Wai Soon
# Ransomhub Tor Browser Scrapper

# Import Libraries
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, List
import csv

# Configure Selenium to use the Tor browser


def configure_tor_browser():
    options = Options()
    options.headless = True
    # This path should point to tor browser executable
    options.binary_location = r'/home/kali/Desktop/start-tor-browser.desktop'
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
    driver.get(url)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.index-anchor')))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    list_div = []

    # Find all divs with the class 'col-12 col-md-6 col-lg-4'
    divs_name = soup.find_all('div', {"class": "col-12 col-md-6 col-lg-4"})
    for div in divs_name:
        try:
            # Extract the date-time string from 'card-footer'
            date_time_str = div.find('div', {"class": "card-footer"}).text.strip()
            # Split to get the date part
            date_str = date_time_str.split()[0]
            # Parse the date string to a datetime object
            card_date = datetime.strptime(date_str, '%Y-%m-%d')

            # Apply the date filter
            if datetime(2024, 1, 1) <= card_date <= datetime(2024, 8, 31):
                # Extract the title and link if the date is within the range
                title_element = div.find('div', {"class": "card-title text-center"})
                if title_element:
                    title = title_element.text.strip()
                else:
                    title = "No title found"
                relative_link = div.find('a')['href']
                # Ensure the link is a complete URL
                link = url + relative_link if not relative_link.startswith("http") else relative_link
                list_div.append({"title": title, "link": link, "date": date_str})
        except Exception as e:
            print(f"Error processing div: {e}")
            pass

    return list_div

# Function to scrape the subpage


def scrape_subpage(driver, subpage_url):
    print(f"Navigating to subpage URL: {subpage_url}")  # Debugging print statement
    driver.get(subpage_url)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.post-content')))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    description = soup.select_one('.post-content').text.strip()
    disclosed_links = [link.text.strip() for link in soup.select('.card-text.text-danger')]
    return description, disclosed_links

# Function to save data to a CSV file


def save_to_csv(data, filename):
    if not data:
        print("No data to save.")
        return

    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


# Saving scrapping results to CSV file for further cleaning
main_page_url = "http://ransomxifxwc5eteopdobynonjctkxxvap77yqifu2emfbecgbqdw6qd.onion/"

driver = configure_tor_browser()
try:
    cards = scrape_main_page(driver, main_page_url)
    if not cards:
        print("No cards found.")
    results = []

    for card in cards:
        subpage_url = card['link']
        description, disclosed_links = scrape_subpage(driver, subpage_url)
        results.append({
            "Name": card['title'],
            "Date": card['date'],
            "Description": description,
            "Disclosed Links": ", ".join(disclosed_links)
        })

    # Save results to CSV
    save_to_csv(results, 'scraped_data.csv')
finally:
    driver.quit()

import requests
from bs4 import BeautifulSoup
import csv
import time
import re

# Configuration
TOR_PROXY = {
    'http': 'socks5h://127.0.0.1:9150',
    'https': 'socks5h://127.0.0.1:9150'
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
                  "AppleWebKit/537.36 (KHTML, like Gecko) " \
                  "Chrome/85.0.4183.121 Safari/537.36"
}

BASE_URL = 'http://mbrlkbtq5jonaqkurjwmxftytyn2ethqvbxfu4rgjbkkknndqwae6byd.onion'  # Base domain
PAGE_PATH = '/index.php?page='  # Page path based on the provided link structure

# Initialize session with Tor proxy
session = requests.Session()
session.proxies.update(TOR_PROXY)
session.headers.update(HEADERS)

def get_soup(url):
    """
    Fetches the content at the given URL and returns a BeautifulSoup object.
    """
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Request error for {url}: {e}")
        return None

def extract_main_page_data(soup):
    """
    Extracts data from the main page's table.
    Returns a list of dictionaries containing the extracted data.
    """
    data = []
    # Updated table selection using regex to match 'width:1200px' in style
    table = soup.find('table', style=lambda s: s and re.search(r'width\s*:\s*1200px', s))
    if not table:
        print("Main table not found!")
        return data

    news_entries = table.find_all('th', class_='News')
    for news in news_entries:
        try:
            # Extract Title from the first child div (assuming the first div holds the title)
            title_div = news.find('div')
            country = title_div.get_text(separator='|').split('|')[0].strip() if title_div else 'N/A'

            # Extract Website
            link_icon = news.find('i', class_='link')
            website = link_icon.next_sibling.strip() if link_icon and link_icon.next_sibling else 'N/A'

            # Extract Views
            views_text = news.find(text=lambda x: x and 'views' in x)
            views = views_text.split(': ')[1].strip() if views_text else 'N/A'

            # Extract Added Date
            added_text = news.find(text=lambda x: x and 'added' in x)
            added_date = added_text.split(': ')[1].strip() if added_text else 'N/A'

            # Extract Publication Date
            pub_text = news.find(text=lambda x: x and 'publication date' in x)
            publication_date = pub_text.split(': ')[1].strip() if pub_text else 'N/A'

            # Extract onclick attribute to get detail identifier
            onclick_value = news.get('onclick', '')
            if not onclick_value:
                print(f"No onclick attribute found for {country}")
                continue
            # Assuming the onclick format is: viewtopic('identifier')
            identifier = onclick_value.split("'")[1] if "'" in onclick_value else None
            if not identifier:
                print(f"Could not parse identifier from onclick for {country}")
                continue

            # Construct detail page URL
            detail_url = f"{BASE_URL}/topic.php?id={identifier}"

           
            data.append({
                'Country': country,
                'Website': website,
                'Views': views,
                'Added Date': added_date,
                'Publication Date': publication_date,
                'Detail URL': detail_url
            })
        except Exception as e:
            print(f"Error extracting data for a news entry: {e}")
            continue
    return data


def extract_detail_page_data(detail_url):
    """
    Extracts company info, download links, and RAR password from the detail page.
    Returns a tuple (title_info, company_info, download_links, rar_password).
    """
    soup = get_soup(detail_url)
    if not soup:
        return ('N/A', 'N/A', 'N/A', 'N/A')
    
    print("Extracting details from:", detail_url)
    try:
        # Extract Title
        title_div = soup.find_all('div') 
        title_info = next((div.get_text(separator='|').strip().split('|')[0] for div in title_div if 'information' in div.text), 'N/A')
        
        # Extract Company Info
        info_div = soup.find_all('div')  
        company_info = next((div.get_text(separator='|').strip().split('|')[7] for div in info_div if 'information' in div.text), 'N/A')

        # Extract Download Links and RAR Password
        download_div = soup.find('div', style=lambda value: value and 'line-height: 1.50' in value)
        download_links = []
        rar_password = 'N/A'
        
        if download_div:
            # Get the text from the div
            text = download_div.get_text(separator='\n')
            # Use regex to find all URLs
            urls = re.findall(r'http[s]?://\S+', text)
            # Assign to download_links
            download_links = urls
            # Extract RAR password using regex
            rar_match = re.search(r'Rar password:\s*(\S+)', text, re.IGNORECASE)
            if rar_match:
                rar_password = rar_match.group(1).strip()

        # Join download links with comma separation
        download_links_str = ', '.join(download_links) if download_links else 'N/A'

        return (title_info, company_info, download_links_str, rar_password)
    except Exception as e:
        print(f"Error extracting detail data from {detail_url}: {e}")
        return ('N/A', 'N/A', 'N/A', 'N/A')



def scrape_website():
    """
    Main function to scrape the website and save data to CSV.
    """
    current_page = 1
    total_pages = 39 

    with open('ransomware_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Country', 'Website', 'Views', 'Added Date', 'Publication Date', 'Company Info', 'Download Links', 'RAR Password'])

        while current_page <= total_pages:
            page_url = f"{BASE_URL}{PAGE_PATH}{current_page}"
            print(f"Scraping page {current_page}: {page_url}")
            soup = get_soup(page_url)
            if not soup:
                print(f"Skipping page {current_page} due to fetch error.")
                current_page += 1
                continue

            page_data = extract_main_page_data(soup)
            print(f"Found {len(page_data)} entries on page {current_page}.")

            for entry in page_data:
                title, company_info, download_links, rar_password = extract_detail_page_data(entry['Detail URL'])
                writer.writerow([
                    title, 
                    entry['Country'],
                    entry['Website'],
                    entry['Views'],
                    entry['Added Date'],
                    entry['Publication Date'],
                    company_info,
                    download_links,
                    rar_password  
                ])
                print(f"Scraped data for {title}")

              
                time.sleep(3)

            current_page += 1

    print("Scraping completed. Data saved to ransomware_data.csv")

if __name__ == "__main__":
    scrape_website()

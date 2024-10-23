import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

# Configure Selenium to use the Tor browser
def configure_tor_browser():
    options = Options()
    options.headless = False  # Set to True if you want to run in headless mode (without opening the browser)
    
    # Path to Tor browser executable (adjust this to where Tor is installed on your system)
    options.binary_location = r'/home/kali/Desktop/torbrowser.desktop'
    
    # Set up Tor's SOCKS5 proxy
    options.set_preference('network.proxy.type', 1)
    options.set_preference('network.proxy.socks', '127.0.0.1')
    options.set_preference('network.proxy.socks_port', 9150)  # Default port for Tor
    options.set_preference('network.proxy.socks_remote_dns', True)

    return webdriver.Firefox(options=options)

# Open the webpage using the Tor browser
driver = configure_tor_browser()

# Accessing the .onion site
try:
    # Open the webpage
    driver.get('http://incblog6qu4y4mm4zvw5nrmue6qbwtgjsxpw6b7ixzssu36tsajldoad.onion/blog/disclosures')
    
    while True:
        try:
            # Try to find the "load more" button
            element = driver.find_element(By.CSS_SELECTOR, "#root .root__container .container .main__container .disclosures__container .more__container.text-primary.cursor-pointer.p-12.text-sm")
            print("Element found!")
            break  # If the element is found, break the loop and continue
        except NoSuchElementException:
            print("Element not found, waiting...")
            time.sleep(5)  # Wait for 5 seconds before checking again

    num_clicks = 0
    # Loop to load more content (if applicable)
    while True:
        try:
            # Find and click the "load more" button
            load_more_button = driver.find_element(By.CSS_SELECTOR, "#root .root__container .container .main__container .disclosures__container .more__container.text-primary.cursor-pointer.p-12.text-sm")
            load_more_button.click()
            num_clicks += 1
            time.sleep(10)  # Adjust the waiting time if needed
        except Exception as e:
            print("No more content to load. Num of clicks: " + str(num_clicks))
            break

    # Extract all links and corresponding country flags from the 'announcement__container' class
    announcement_containers = driver.find_elements(By.CSS_SELECTOR, "#root .root__container .container .main__container .disclosures__container .announcement__container")
    links_and_flags = [(container.get_attribute('href'), container.find_element(By.CSS_SELECTOR, ".flex-col.justify-between.items-end .w-24.h-24").get_attribute('src')) for container in announcement_containers]
    print("Extracted " + str(len(links_and_flags)) + " items.")

    # Prepare CSV file to store victim data
    with open('victim_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Victim Name', 'Data Types', 'Date', 'Country Flag', 'Description', 'Revenue']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|')
        writer.writeheader()
    
        # Now, for each link, visit the page and scrape the necessary data
        # for link in links:
        for link, flag_url in links_and_flags:
            driver.get(link)
            
            while True:
                try:
                    child_page = driver.find_element(By.CSS_SELECTOR, "#root .root__container .container .main__container .disclosure__container .announcement__el .action__container .new__el .flex .text-muted .text-white.text-md").text
                    print("Child page loaded: " + child_page)
                    break  # If the element is found, break the loop and continue
                except NoSuchElementException:
                    print("Child page loading...")
                    time.sleep(2)  # Wait for 3 seconds before checking again

            # Extract the victim name
            try:
                victim_name = driver.find_element(By.CSS_SELECTOR, "#root .root__container .container .main__container .disclosure__container .announcement__el .action__container .new__el .flex .text-muted .text-white.text-md").text
            except Exception as e:
                print(f"Error finding victim name for {link}: {e}")
                victim_name = 'N/A'
    
            # Extract the date from the class 'ml-8'
            try:
                date = driver.find_element(By.CSS_SELECTOR, "#root .root__container .container .main__container .disclosure__container .announcement__el .action__container .new__el .flex .text-muted .ml-8").text
            except Exception as e:
                print(f"Error finding date for {link}: {e}")
                date = 'N/A'
    
            # Extract description
            try:
                # Find all span elements
                description_elements = driver.find_elements(By.CSS_SELECTOR, "#root .root__container .container .main__container .disclosure__container .announcement__el .action__container .new__el .text-white.text-sm.break-words")

                # Extract text from each span element and join them with a newline
                description = '\n'.join([element.text for element in description_elements])

                # Handle cases where no description is found
                if not description:
                    description = 'N/A'
            except Exception as e:
                print(f"Error finding description for {link}: {e}")
                description = 'N/A'

            # Extract revenue
            try:
                revenue = driver.find_element(By.CSS_SELECTOR, "#root .root__container .container .main__container .disclosure__container .announcement__el .action__container .new__el .text-sm.text-white.mb-4").text
            except Exception as e:
                print(f"Error finding revenue for {link}: {e}")
                description = 'N/A'
            

            # Extract all data types under each popover__container
            try:
                popover_containers = driver.find_elements(By.CSS_SELECTOR, "#root .root__container .container .main__container .disclosure__container .announcement__el .action__container .new__el .flex .popover__container.mr-4")
                data_types = []
                for popover in popover_containers:
                    # data_type = popover.find_element(By.CLASS_NAME, 'popover__message.text-xs').text
                    # data_types.append(data_type)
                    data_type = popover.find_element(By.CSS_SELECTOR, "span.popover__message.text-xs").get_attribute('textContent')
                    if data_type == "Proof" or data_type == "Encrypted":
                        pass
                    elif data_type.strip():  # Ensure it's not an empty or whitespace string
                        data_types.append(data_type.strip())  # Strip whitespace

                # If no valid data types were found, append 'N/A' to indicate that no data was available
                if not data_types:
                    data_types.append('N/A')

                # Join all data types into a single string separated by commas
                data_types_str = ', '.join(data_types)
                # Extract the country code from the flag URL (e.g., 'US' from 'https://flagsapi.com/US/flat/64.png')
                country_code = flag_url.split('/')[-3]
                
                # Write the victim name, data types, date and country flag in the same row
                writer.writerow({'Victim Name': victim_name, 'Data Types': data_types_str, 'Date': date, 'Country Flag': country_code, 'Description': description, 'Revenue': revenue})
                print(f"Data extracted for: {victim_name}")
            except Exception as e:
                print(f"Error extracting data types for {link}: {e}")
    
finally:
    # Clean up
    driver.quit()
    print("Browser closed")

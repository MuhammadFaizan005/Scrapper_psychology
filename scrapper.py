from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import re  # Import the regular expressions module

file_path = "eMAILS - Sheet1.csv"
df = pd.read_csv(file_path)
Links = df["LINKS"]

def extract_emails_from_page(url, driver):
    driver.get(url)
    
    # Find email addresses on the page
    page_source = driver.page_source
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', page_source)
    
    # Print found emails
    print(f"Emails found on {url}:")
    for email in emails:
        print(email)

def extract_and_find_emails(url, driver):
    driver.get(url)
    
    # Find the specific div with class "controls"
    div_element = driver.find_element(By.CLASS_NAME, 'controls')
    
    # Find the anchor tag within the div and extract its href attribute
    anchor = div_element.find_element(By.TAG_NAME, 'a')
    href = anchor.get_attribute('href')
    
    # Print the href
    print(f"Found href: {href}")
    
    # Extract emails from the href page
    extract_emails_from_page(href, driver)

# Set up Chrome options (without headless mode)
options = webdriver.ChromeOptions()
# You can add any options if needed, for now, no options are added

# Start the WebDriver and keep the browser open
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Process each link from the CSV file
    for url in Links:
        extract_and_find_emails(url, driver)

finally:
    # Keep the browser open until all URLs are processed
    print("Processing complete. Closing the browser.")
    driver.quit()

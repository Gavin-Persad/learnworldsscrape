import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

def login(driver, login_url, username, password):
    # Navigate to the login page
    driver.get(login_url)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'menuItem5'))).click()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'js-signin-input')))
    
    # Log in
    driver.find_element(By.CLASS_NAME, '-email-input').send_keys(username)
    driver.find_element(By.CLASS_NAME, '-pass-input').send_keys(password)
    driver.find_element(By.CLASS_NAME, '-login-but').click()
    time.sleep(5)  # Adjust as needed for loading

def scrape_page(driver, output_folder):
    # Locate the iframe and switch to it
    iframe = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.ID, 'playerFrame'))
    )
    driver.switch_to.frame(iframe)
    
    # Parse iframe content
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    inner_content = soup.body
    
    # Extract title for filename
    page_title = soup.find('title').get_text(strip=True)
    filename = f"{output_folder}/{page_title.replace(' ', '_')}.mdx"
    
    # Extract text content and save as Markdown
    if inner_content:
        content = inner_content.get_text(separator='\n', strip=True)
        markdown_content = f"## {page_title}\n\n{content}"
        
        with open(filename, 'w', encoding='utf-8') as mdx_file:
            mdx_file.write('---\n')
            mdx_file.write(f'title: "{page_title}"\n')
            mdx_file.write('---\n\n')
            mdx_file.write(markdown_content)
    
    # Optional: Save prettified HTML to a file for debugging
    with open('pretty_output.html', 'w', encoding='utf-8') as html_file:
        html_file.write(soup.prettify())

    # Switch back to the main page
    driver.switch_to.default_content()
    print(f"Content for '{page_title}' saved to {filename}")

def navigate_and_scrape_all_pages(url, output_folder):
    login_url = os.getenv('LOGIN_URL')
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    chromedriver_path = os.getenv('CHROMEDRIVER_PATH')

    # Set up Selenium with ChromeOptions
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless if needed
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Log in
    login(driver, login_url, username, password)
    
    # Navigate to the first page
    driver.get(url)
    time.sleep(5)  # Adjust as needed for loading
    
    # Loop through all pages
    while True:
        # Scrape current page
        scrape_page(driver, output_folder)
        
        try:
            # Click the "Next" button
            next_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
            )
            next_button.click()
            time.sleep(5)  # Wait for the next page to load
            
        except Exception as e:
            # If "Next" button is not found or clickable, assume end of pages
            print("End of pages or 'Next' button not found.")
            break
    
    driver.quit()
    print("All pages scraped.")

# Usage
output_folder = "scraped_content"  # Folder to save all scraped pages
os.makedirs(output_folder, exist_ok=True)

navigate_and_scrape_all_pages(
    'https://learn.schoolofcode.co.uk/path-player?courseid=bc17-we&unit=66b4c307c0dc4aaa0f0cdfbbUnit', 
    output_folder
)
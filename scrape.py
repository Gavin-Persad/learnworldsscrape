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
import re

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

def clean_mdx_file(file_path):
    # Define the start and end phrases
    start_phrase = "Learn to code, change your life!"
    end_phrase = "Cookie preferences"
    
    # Read the content of the MDX file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Use regular expressions to remove everything between the start and end phrases
    pattern = re.compile(re.escape(start_phrase) + r'.*?' + re.escape(end_phrase), re.DOTALL)
    cleaned_content = re.sub(pattern, '', content)
    
    # Save the cleaned content back to the MDX file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

def scrape_page(driver, output_folder, page_number):
    # Locate the iframe and switch to it
    iframe = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.ID, 'playerFrame'))
    )
    driver.switch_to.frame(iframe)
    
    # Get iframe content as a string
    html_content = driver.page_source
    
    # Parse iframe content
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    inner_content = soup.body
    
    # Extract title for filename
    page_title = soup.find('title').get_text(strip=True)
    sanitized_title = page_title.replace(' ', '_').replace('/', '_')
    markdown_filename = f"{output_folder}/{page_number:03d}_{sanitized_title}.mdx"
    html_filename = f"{output_folder}/{page_number:03d}_{sanitized_title}.html"
    
    # Extract text content and save as Markdown
    if inner_content:
        content = inner_content.get_text(separator='\n', strip=True)
        markdown_content = f"## {page_title}\n\n{content}"
        
        with open(markdown_filename, 'w', encoding='utf-8') as mdx_file:
            mdx_file.write('---\n')
            mdx_file.write(f'title: "{page_title}"\n')
            mdx_file.write('---\n\n')
            mdx_file.write(markdown_content)
    
    # Optional: Save prettified HTML to a file for debugging
    with open(html_filename, 'w', encoding='utf-8') as html_file:
        html_file.write(soup.prettify())
        html_file.write(f'title: "{page_title}"\n')
        html_file.write(str(soup))

    # Switch back to the main page
    driver.switch_to.default_content()
    print(f"Content for '{page_title}' saved to {markdown_filename}")
    
    # Clean the MDX file
    clean_mdx_file(markdown_filename)

# def take_screenshot(driver, output_folder, page_number):
#     screenshot_path = os.path.join(output_folder, f"page_{page_number}.png")
#     driver.save_screenshot(screenshot_path)
#     print(f"Screenshot saved to {screenshot_path}")

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
    # Keep track of the current page
    current_page = 1
    
    # Loop through all pages
    while True:
                
        
        # Scrape current page
        scrape_page(driver, output_folder, current_page)
        
        try:
            # Switch back to the main page
            driver.switch_to.default_content()
            # Take a screenshot of the current page
            # take_screenshot(driver, output_folder, current_page)

            # Click the "Next" button
            print("Looking for the 'Next' button...")
            next_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'default-course-player-nav-btn-lbl') and contains(text(), 'next')]"))
)
            print("Found the 'Next' button, clicking it...")
            next_button.click()
            current_page += 1
            print(f"Navigated to page {current_page}")
            time.sleep(5)  # Wait for the next page to load
            
        except Exception as e:
            # If "Next" button is not found or clickable, assume end of pages
            print(f"End of pages or 'Next' button not found. Exception: {e}")
            break
    
    driver.quit()
    print("All pages scraped.")

# Usage
output_folder = "scraped_content"  # Folder to save all scraped pages
os.makedirs(output_folder, exist_ok=True)

navigate_and_scrape_all_pages(
    'https://learn.schoolofcode.co.uk/path-player?courseid=ai-and-data-experience-bc-17&unit=66e2e3d9366f76d2290fda40Unit', 
    output_folder
)
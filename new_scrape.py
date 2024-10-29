from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get('https://learn.schoolofcode.co.uk/path-player?courseid=bc17-we&unit=66b4c307c0dc4aaa0f0cdfbbUnitS')  # Replace with the actual URL

# Create a folder to save the files
output_folder = 'scraped_content'
os.makedirs(output_folder, exist_ok=True)

while True:
    try:
        # Get the iframe's page source and parse it with BeautifulSoup
        iframe_source = driver.page_source
        soup = BeautifulSoup(iframe_source, 'html.parser')

        # Locate the target <div> inside the iframe content
        inner_content = soup.body  # Assuming content is within <body> tag

        if inner_content:
            # Extract and clean up all content as text, maintaining structure
            content = inner_content.get_text(separator='\n', strip=True)
            print(content)  # Print or save it as needed

            # Extract the title for the filename
            title = soup.title.string.strip().replace(' ', '_')  # Adjust as needed
            output_file = os.path.join(output_folder, f"{title}.mdx")

            # Convert to Markdown (simple example)
            markdown_content = f"## Extracted Content\n\n{content}"

            # Save to an MDX file with front matter
            with open(output_file, 'w', encoding='utf-8') as mdx_file:
                mdx_file.write('---\n')
                mdx_file.write(f'title: "{title}"\n')
                mdx_file.write('---\n\n')
                mdx_file.write(markdown_content)
        else:
            raise ValueError("Content within iframe not found")

        # Find and click the "next" button
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='next']"))
        )
        next_button.click()

    except Exception as e:
        print(f"An error occurred: {e}")
        break

# Close the WebDriver
driver.quit()
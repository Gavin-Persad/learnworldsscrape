# Web Scraping Script

This script logs into a specified website, navigates to a target page, and extracts the inner text of a specific `<div>` element. The extracted content is then saved as MDX and HTML files with front matter.

## Dependencies

The script requires the following Python packages:

- `selenium`
- `beautifulsoup4`
- `python-dotenv`

These dependencies are listed in the `requirements.txt` file.

## Installation

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create a virtual environment.

   ```bash
   pip install virtualenv
   python -m venv venv
   ```

4. Install ChromeDriver:
   https://developer.chrome.com/docs/chromedriver/downloads

5. Install the required dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

6. Create a `.env` file in the project directory with the following environment variables:

   ```env
   LOGIN_URL=your_login_url
   USERNAME=your_username
   PASSWORD=your_password
   CHROMEDRIVER_PATH=path_to_your_chromedriver
   ```

7. For Mac users only:
   If you run into an issue accessing ChromeDriver, run the following command:

   ```bash
   xattr -d com.apple.quarantine chromedriver
   ```

## Usage

At the bottom of the scrape.py file there is a `navigate_and_scrape_all_pages` function being called. Within this function, input the chosen URL for the module you want to scrape into the '' (single quotations). This URL will be the starting point, and the script will scrape this page then crawl and scrape any other page after it within the module.

### Example

```
navigate_and_scrape_all_pages(
    'https://learn.schoolofcode.co.uk/path-player?courseid=ai-and-data-experience-bc-17&unit=66e2e3d9366f76d2290fda40Unit',
    output_folder
)
```

After selecting your chosen URL:

1. Open a terminal and navigate to the project directory.
2. Run the script using Python:

   ```bash
   python scrape.py
   ```

   The script will log into the specified website, navigate to the target page, and extract the inner text of the specified `<div>` element. The extracted content will be saved as MDX and HTML files in the `scraped_content` directory.

3. Press `ctl c` to terminate the process any time.

## Output

The extracted content will be saved in the `scraped_content` directory with filenames based on the page titles. Each page will have both an MDX file and an HTML file for debugging purposes.

## Example

To run the script, use the following command:

```bash
python scrape.py
```

This will execute the script and save the extracted content to the `scraped_content` directory.

## Contributors

School of Code Fellows:

- Alexander Carr (Bootcamp 15) [LinkedIn](https://www.linkedin.com/in/alexander-carr-424591144/) | [Github](https://github.com/1alexc)
- Annamaria Koutsoras (Bootcamp 16) [LinkedIn](https://www.linkedin.com/in/annamariakou/) | [Github](https://github.com/annamariakou)
- Arseniy Panin (Bootcamp 16) [LinkedIn](https://www.linkedin.com/in/arseniy-panin-a6583a161/) | [Github](https://github.com/arseniyus)
- Gavin Persad (Bootcamp 16) [LinkedIn](https://www.linkedin.com/in/gavin-persad/) | [Github](https://github.com/Gavin-Persad)
- Winnie Lau (Bootcamp 16) [LinkedIn](https://www.linkedin.com/in/lau-winnie) | [Github](https://github.com/lazycloud0)

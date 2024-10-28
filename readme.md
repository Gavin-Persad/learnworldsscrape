# Web Scraping Script

This script logs into a specified website, navigates to a target page, and extracts the inner text of a specific `<div>` element. The extracted content is then saved as an MDX file with front matter.

## Dependencies

The script requires the following Python packages:

- `selenium`
- `beautifulsoup4`
- `python-dotenv`

These dependencies are listed in the `requirements.txt` file.

## Installation

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using pip:

```bash
  pip install -r requirements.txt
```

4. Environment Variables

Create a `.env` file in the project directory with the following environment variables:

```env
LOGIN_URL=your_login_url
USERNAME=your_username
PASSWORD=your_password
CHROMEDRIVER_PATH=path_to_your_chromedriver
```

## Usage

1. Open a terminal and navigate to the project directory.
2. Run the script using Python:

```bash
python scrape.py
```

The script will log into the specified website, navigate to the target page, and extract the inner text of the specified `<div>` element.
The extracted content will be saved as an MDX file named `output.mdx` in the project directory.

## Output

The extracted content will be saved in a file named `output.mdx` in the project directory. - Additionally, a prettified HTML file named `pretty_output.html` will be saved in the project directory for debugging purposes.

## Example To run the script, use the following command:

```bash
python scrape.py

This will execute the script and save the extracted content to output.mdx.
```

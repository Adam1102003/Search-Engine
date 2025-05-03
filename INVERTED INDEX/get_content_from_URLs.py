import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import os

# Specify the directory to save the files
output_dir = "2"
os.makedirs(output_dir, exist_ok=True)

# Open the file and read the URLs
with open('cleaned/cleaned_links_2.txt', 'r') as f:
    urls = [line.strip() for line in f]

# Define retry strategy
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504],
)

# Create an HTTP adapter with retry strategy
adapter = HTTPAdapter(max_retries=retry_strategy)

# Create a session with the adapter
session = requests.Session()
session.mount("https://", adapter)
session.mount("http://", adapter)

for url in urls:
    try:
        response = session.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Create a filename by replacing special characters in URL
        filename = url.replace("https://", "").replace("/", "_").replace(".", "__").replace(':','___') + ".txt"
        filepath = os.path.join(output_dir, filename)

        # Extract text from the webpage
        text = soup.get_text()

        # Save the text to a file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)

        print(f"Saved content of {url} to {filepath}")
    except requests.exceptions.RequestException as e:
        print(f"Request error occurred while processing {url}: {e}")
    except Exception as e:
        print(f"General error occurred while processing {url}: {e}")
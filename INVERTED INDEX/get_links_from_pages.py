from bs4 import BeautifulSoup
import urllib.request
import urllib.parse

parser = 'lxml'  

url = "https://www.foxnews.com/tech"

try:
    resp = urllib.request.urlopen(url)
    soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
except Exception as e:
    print(f"Error fetching the URL: {e}")
    exit()

unique_links = set()

try:
    with open("links/links_3.txt", "w") as file:
        for link in soup.find_all('a', href=True):
            href = link['href']
            if not href.startswith('http'):
                href = urllib.parse.urljoin(url, href)
            if href.startswith('https') and href not in unique_links:
                unique_links.add(href)
                file.write(href + "\n")
except Exception as e:
    print(f"Error writing to file: {e}")

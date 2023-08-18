import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Create data folder if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

base_url = 'https://cdeiuk.github.io/ai-assurance-guide/'

# Fetch the content of the main page
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Save the main page
with open(os.path.join('data', 'index.html'), 'wb') as f:
    f.write(response.content)

# Find all the linked pages in the main page
for link in soup.find_all('a', href=True):
    href = link['href']
    print(href)

    # Check if the link is relative and make it absolute
    absolute_link = urljoin(base_url, href)

    # Skip links that point to a different domain
    if urlparse(absolute_link).netloc != urlparse(base_url).netloc:
        continue

    # Fetch the linked page content
    response = requests.get(absolute_link)

    # Create a file name using the last part of the URL
    filename = urlparse(href).path.strip('/').split('/')[-1] or 'index'

    # Ensure the filename ends with .html
    if not filename.endswith('.html'):
        filename += '.html'

    # Save the linked page
    with open(os.path.join('data', filename), 'wb') as f:
        f.write(response.content)

print("Downloaded webpages saved to 'data' folder.")

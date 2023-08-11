import os
from urllib.parse import urlparse
import twitter,medium

# Twitter scraping code
def scrape_twitter(url):
    # Your Twitter scraping code here
    # ...
    # Extract and return links
    links = []
    # Code to extract links
    return links

# Medium scraping code
def scrape_medium(url):
    # Your Medium scraping code here
    # ...
    # Extract and return links
    links = []
    # Code to extract links
    return links

# Get host name and unique key from URL
def get_host_and_key(url):
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    key = parsed_url.path.split('/')[-1].split('?')[0] if host == 'twitter.com' else ''
    return host, key

# Ask user for the input of the page link
url = input("Enter the page link you want to scrape: ")

# Get host name and unique key
host, key = get_host_and_key(url)

# Check host name and execute corresponding scraping code
if host == 'twitter.com':
    links = twitter.scrape_twitter(url)
elif host == 'medium.com':
    links = medium.scrape_medium(url)
else:
    print("Host not matched.")
    links = []

# Create directory based on the host name
directory = os.path.join("links_directory", host)
os.makedirs(directory, exist_ok=True)

# Save links into a file
if links:
    file_path = os.path.join(directory, host + '_' + key + ".txt")
    with open(file_path, "w") as file:
        for link in links:
            file.write(link + "\n")

    print("Links saved successfully in:", file_path)

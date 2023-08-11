from selenium import webdriver
from bs4 import BeautifulSoup

def scrape_medium(url):
    # Configure Selenium webdriver
    driver = webdriver.Chrome()  # Replace with the appropriate webdriver for your browser
    print("Scraping")
    driver.get(url)

    # Get the page source after JavaScript execution
    page_source = driver.page_source

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all articles on the page
    articles = soup.find_all('article')

    # Extract links within the text of each article
    links = set()
    for article in articles:
        article_links = article.find_all('a')
        for link in article_links:
            href = link.get('href')
            if href and "signin?" not in href:
                links.add(href)

    return links
    # Close the Selenium webdriver
    driver.quit()

    
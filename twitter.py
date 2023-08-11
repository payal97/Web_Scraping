import os
import re
from parsel import Selector
from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Page
from urllib.parse import urlparse



def extract_links_from_text(text):
    # Find all URLs within the text
    urls = re.findall(r'https?://\S+', text)
    return urls 


def parse_tweets(selector: Selector):
    """
    parse tweets from pages containing tweets like:
    - tweet page
    - search page
    - reply page
    - homepage
    returns list of tweets on the page where 1st tweet is the 
    main tweet and the rest are replies
    """
    results = []
    tweets = selector.xpath("//article[@data-testid='tweet']")
    for i, tweet in enumerate(tweets):
        found = {
            # other attributes...
            "text": "".join(tweet.xpath(".//*[@data-testid='tweetText']//text()").getall()),
            # other attributes...
        }
        # Extract links from tweet text
        found["links"] = extract_links_from_text(found["text"])
        
        # main tweet (not a reply):
        if i == 0:
            # Extract links from main tweet's comments
            comments = tweet.xpath(".//div[@data-testid='tweet']//div[@lang]")
            comment_links = []
            for comment in comments:
                text = "".join(comment.xpath(".//text()").getall())
                comment_links.extend(extract_links_from_text(text))
            found["comment_links"] = comment_links
            
            # other attributes...
        
        results.append({k: v for k, v in found.items() if v is not None})
    return results

def scrape_tweet(url: str, page: Page):
    page.set_default_timeout(60000)
    """
    Scrape tweet and replies from tweet page like:
    https://twitter.com/Scrapfly_dev/status/1587431468141318146
    """
    # go to url
    page.goto(url)
    # wait for content to load
    page.wait_for_selector("//article[@data-testid='tweet']")  
    # retrieve final page HTML:
    html = page.content()
    # Extract links from HTML
    #print(links)
    # parse it for data:
    selector = Selector(html)
    tweets = parse_tweets(selector)
    return tweets

# example run:
def scrape_twitter(link):
    with sync_playwright() as pw:

        # Ask user for the input of the page link
        page_link = link
        # start browser and open a new tab:
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})


        # scrape tweet and replies:
        print("Scraping...")
        tweet_and_replies = scrape_tweet(page_link, page)

        # Extract links from tweet_and_replies
        all_links = []
        for tweet in tweet_and_replies:
            if "links" in tweet:
                all_links.extend(tweet["links"])
            if "comment_links" in tweet:
                all_links.extend(tweet["comment_links"])

    return all_links

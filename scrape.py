
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re
from sentiment import analyze_sentiments

def scrape_website(base_url, max_pages=4):
    """Scrape multiple review pages from a Flipkart product."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    all_reviews_html = "       \n\n"

    try:
        for page_num in range(1, max_pages + 1):
            page_url = f"{base_url}&page={page_num}"
            print(f"Scraping: {page_url}")
            driver.get(page_url)
            time.sleep(3)  # Allow JS to load reviews

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            review_divs = soup.find_all('div', class_='ZmyHeo')  # review text container

            if not review_divs:
                print("No more reviews found. Ending.")
                break

            # for div in review_divs:
            #     review_text = div.get_text(strip=True)
            #     all_reviews_html += review_text + "\n\n"
            for i, div in enumerate(review_divs, start=1):
                review_text = div.get_text(strip=True)
                sentiment_output = analyze_sentiments(review_text)
                spacing11="     "
                all_reviews_html += f"{i}. {review_text} {sentiment_output} {spacing11}  \n\n"


    finally:
        driver.quit()

    return all_reviews_html.strip()


def extract_body_content(dom_content):
    """No longer used (since scrape_website gets review text), but kept for compatibility."""
    return dom_content  # Already pre-cleaned in scrape_website


def clean_body_content(text):
    """Clean the text by removing non-ASCII characters and extra spaces."""
    cleaned = re.sub(r'\s+', ' ', text)
    cleaned = re.sub(r'[^\x00-\x7F]+', '', cleaned)
    return cleaned.strip()


def split_dom_content(content, chunk_size=2000):
    """Split long content into chunks for LLM input."""
    return [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]


# --------------------------------------------------------------------------------------------------------------

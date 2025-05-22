# from selenium.webdriver import Remote, ChromeOptions
# from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup

# AUTH = 'brd-customer-hl_1306e5d9-zone-ai_scraper:cdi9r919fian'
# SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

# def scrape_website(website):
#     print('Connecting to Browser API...')
#     sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
#     with Remote(sbr_connection, options=ChromeOptions()) as driver:
#         driver.get(website)
#         print('Taking page screenshot to file page.png')
#         driver.get_screenshot_as_file('./page.png')
#         print('Navigated! Scraping page content...')
#         html = driver.page_source
#         return html


# def extract_body_content(html_content):
#     soup=BeautifulSoup(html_content,"html.parser")
#     body_content=soup.body
#     if body_content:
#         return str(body_content)
#     return ""

# def clean_body_content(body_content):
#     soup=BeautifulSoup(body_content,"html.parser")
    
#     for script_or_style in soup(["script","style"]):
#         script_or_style.extract()
        
#     cleaned_content=soup.get_text(separator="\n")
#     cleaned_content="\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    
#     return cleaned_content



# def split_dom_content(dom_content, max_length=6000):
#     return[
#         dom_content[i:i+max_length] for i in range(0,len(dom_content),max_length)
#     ]
    
    # -----------------------------------------------------------------------------------------------------------------------
    
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup
# import time
# import re

# def scrape_website(url):
#     """Launch the browser, open the URL, and return full page HTML."""
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
    
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     driver.get(url)
#     time.sleep(3)  # wait for content to load

#     page_source = driver.page_source
#     driver.quit()
#     return page_source

# # def extract_body_content(dom_content):
# #     """Extract all text from the <body> tag using BeautifulSoup."""
# #     soup = BeautifulSoup(dom_content, 'html.parser')
# #     body = soup.find('body')
# #     return body.get_text(separator='\n') if body else "No <body> tag found."
# def extract_body_content(dom_content):
#     """Extract Flipkart product reviews by targeting specific HTML classes."""
#     soup = BeautifulSoup(dom_content, 'html.parser')
    
#     # Extract review texts
#     review_divs = soup.find_all('div', class_='ZmyHeo')
#     reviews = [div.get_text(strip=True) for div in review_divs if div.get_text(strip=True)]
    
#     return '\n\n'.join(reviews) if reviews else "No reviews found."

# def clean_body_content(text):
#     """Clean the body text by removing non-ASCII characters and excessive whitespace."""
#     cleaned = re.sub(r'\s+', ' ', text)
#     cleaned = re.sub(r'[^\x00-\x7F]+', '', cleaned)
#     return cleaned.strip()

# def split_dom_content(content, chunk_size=2000):
#     """Split long content into chunks for LLM input."""
#     return [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]


# ------------------------------------------------------
# all pages review fix number of pages 

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

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor
import time
import logging

logger = logging.getLogger(__name__)

def get_text(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # run headlessly
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        time.sleep(2)  # wait for the page to load

        try:
            accept_button = driver.find_element(By.XPATH, "//span[normalize-space(text())='Zaakceptuj wszystko']")
            accept_button.click()
            time.sleep(1)  # wait for the cookie wall to disappear
        except Exception as e:
            logger.info("Cookie consent not found or already accepted")

        # Get article title
        try:
            title = driver.title
        except:
            title = "Untitled Article"

        # Get article text
        article_text = driver.find_element(By.TAG_NAME, "body").text

        return {
            'title': title,
            'url': url,
            'source': url.split('/')[2],  # Extract domain as source
            'content': article_text
        }
    except Exception as e:
        logger.error(f"Error extracting article from {url}: {str(e)}")
        return None
    finally:
        driver.quit()

def extract_articles_parallel(urls, max_workers):
    """Runs get_text in parallel using ThreadPoolExecutor."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(get_text, urls))
    
    # Filter out None results and return list of article dictionaries
    articles = [article for article in results if article is not None]
    logger.info(f"Successfully extracted {len(articles)} articles from {len(urls)} URLs")
    return articles
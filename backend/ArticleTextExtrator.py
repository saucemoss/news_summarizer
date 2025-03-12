from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor
import time

def get_text(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # run headlessly
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)  # replace with your article URL
    time.sleep(1)  # wait for the page to load

    try:
        accept_button = driver.find_element(By.XPATH, "//span[normalize-space(text())='Zaakceptuj wszystko']")
        accept_button.click()
        time.sleep(1)  # wait for the cookie wall to disappear
    except Exception as e:
        print("Cookie consent not found or already accepted:", e)

    article_text = driver.find_element(By.TAG_NAME, "body").text
    driver.quit()
    return article_text

def extract_articles_parallel(urls, max_workers=4):
    """Runs get_text in parallel using ThreadPoolExecutor."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(get_text, urls)
    # Concatenate all article texts into a single string
    full_text = "\n\n".join(results)
    return full_text
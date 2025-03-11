from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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


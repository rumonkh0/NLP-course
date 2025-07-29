from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json
import re
import time
import os

# Setup ChromeDriver for Colab
# !apt-get update
# !apt install chromium-chromedriver
# !cp /usr/lib/chromium-browser/chromedriver /usr/bin
# os.environ['PATH'] += os.pathsep + '/usr/bin/chromedriver'

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.page_load_strategy = "none"
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Initialize the driver
driver = webdriver.Chrome(options=chrome_options)
link = 'https://www.vfsglobal.com/en/individuals/index.html'

driver.get(link)

def scroll_page():
    total_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(1, total_height, 100):
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(0.1)

time.sleep(2)   

#try for accepting cookies
try:
    accept_cookie = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div/div/div[2]/div/div/button[2]"))
    )
    accept_cookie.click()
    print("✅ Cookie overlay dismissed.")
except Exception as e:
    print("⚠️ Could not click cookie accept button:", e)



for i in range(245):
    print(f"{i + 1}")
    from_country=""
    fromxpath = f"/html/body/div[1]/div[3]/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div[4]/ul/li/div/ul/li[{i+1}]"
    rightxpath = "/html/body/div[1]/div[3]/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div[3]"

    try:
        clkele = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, rightxpath))
        )
        clkele.click()
        # print("dropdown Clicked successfully!")
        # Wait until the element is clickable (max 10 seconds)
        element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, fromxpath))
        )
        text_div = element.find_element(By.XPATH, './/div[contains(@class, "text")]')
        WebDriverWait(driver, 3).until(lambda d: text_div.text.strip() != "")
        from_country = text_div.text.strip()
        # print("Country found:", from_country)
        element.click()
        # print("Clicked successfully!")
        # time.sleep(2)
        # print("-"* 20)
    except Exception as e:
        print("Failed to click:", e)
    # time.sleep(2)

    left_xpath = "/html/body/div[1]/div[3]/div/div[2]/div[1]/div/div[1]/div/div[2]/div/div[3]/div"
    ul_xpath =   "/html/body/div[1]/div[3]/div/div[2]/div[1]/div/div[1]/div/div[2]/div/div[4]/ul/li/div/ul"
    

    WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, left_xpath))
        ).click()
    ul_element = driver.find_element(By.XPATH, ul_xpath)
    # time.sleep(2)
    # Step 2: Find all LI children
    li_elements = ul_element.find_elements(By.TAG_NAME, "li")

    # Extract the country name from <div class="text"> inside each LI
    for i, li in enumerate(li_elements, start=1):
        try:
            text_div = li.find_element(By.XPATH, './/div[contains(@class, "text")]')
            
            # Wait until text appears (max 3s)
            WebDriverWait(driver, 3).until(lambda d: text_div.text.strip() != "")

            country_name = text_div.text.strip()
            # print(f"{i}. {country_name}")
            if country_name == "": print(f"No country name found --------------------------------------------- {from_country}")
            if country_name == "Belarus":
                print(f"{from_country} - {country_name}")
                continue
        except Exception as e:
            print(f"[No country name found] – {e}")
    # print("+" * 20)

driver.quit()
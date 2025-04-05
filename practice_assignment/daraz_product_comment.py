from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.page_load_strategy = "none"
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Initialize the driver
driver = webdriver.Chrome(options=chrome_options)
link = 'https://www.daraz.com.bd/products/c001-i347762802-s1703060973.html'
link = 'https://www.daraz.com.bd/products/men-shoes-luxury-trendy-casual-slip-on-formal-loafers-men-black-male-driving-shoes-i461336579-s2208609434.html'

driver.get(link)

def scroll_page():
    total_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(1, total_height, 100):
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(0.1)

time.sleep(10)
scroll_page()
time.sleep(5)

comments = []

while True:
    for i in range(1, 6):
        try:
            comment = driver.find_element(By.XPATH, f'//*[@id="module_product_review"]/div/div/div[3]/div[1]/div[{i}]/div[3]/div[1]').text
            comments.append(comment)
        except:
            pass

    try:
        button = driver.find_element(By.XPATH, '//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/button[2]')
        print('button found: ', button)
        is_disabled = button.get_attribute('disabled') is not None
        print('is_disabled CHECK', is_disabled)
        if is_disabled:
            print("All comment scrapped.")
            break
        else:
            # button.click()
            driver.execute_script("arguments[0].click();", button)
            time.sleep(1)
            print('Next button clicked.')
    except:
        print("ERROR: Cannot find next button")
        break

# //*[@id="module_product_qna"]/div/div[2]/div[2]/div[2]/div/button[2]
df = pd.DataFrame({'comment':comments})
df.to_csv('comments.csv', index=False)
# for comment in comments:
#     print(comment)
data_dict = df.to_dict(orient='list')
with open('comments.json', 'w', encoding='utf-8') as f:
    json.dump(data_dict, f, ensure_ascii=False, indent=4)

driver.quit()

# /html/body/div[5]/div/div[10]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/button[2]
# /html/body/div[5]/div/div[10]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/button[2]
# /html/body/div[5]/div/div[10]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/button[2]
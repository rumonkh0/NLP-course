from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import math
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
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Initialize the driver
driver = webdriver.Chrome(options=chrome_options)
# query = 'laptop shop near me'
query = input("Enter your search term:  ")
link = f"https://www.google.com/search?tbm=lcl&q={query.replace(' ', '+')}"
driver.get(link)
time.sleep(5)

names = []
mobile_numbers = []
count = 0
page = 0
total = 100

while True:
    page += 1
    print('scripping page-------------------------------------', page)
    for i in range(1, 21):
        c = str(i*2)
        try:
            name = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[7]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div{ '/div' if page != 1 else '' }/div[1]/div[3]/div[{c}]/div[2]/div/div/a[1]/div/div/div[1]/span').text
            div_element = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[7]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div{ '/div' if page != 1 else '' }/div[1]/div[3]/div[{c}]/div[2]/div/div/a[1]/div/div/div[4]')
            div_text = div_element.text
            span_elements = div_element.find_elements(By.TAG_NAME, "span")
            phone_text = div_text.replace(span_elements[0].text, "")
            mobile_number = re.sub(r'\D', '', phone_text)
            print(div_text)
            print(mobile_number)
            print('-------------------')

            if mobile_number:
                names.append(name)
                mobile_numbers.append(mobile_number)
                count += 1
                if count >= total:
                    print("Reached the total count. Creating csv file...")
                    break
        except:
            print("Error to find element")
    if count >= total:
            print("Reached the total count. Creating csv file...")
            break   
    try:
        next_button = driver.find_element(By.XPATH, '//*[@id="pnnext"]/span[2]')
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(3)  # Wait for the next page to load
    except Exception as e:
        print("Next button not found. Creating csv")
        break
    time.sleep(5)

df = pd.DataFrame({"Name": names, "Mobile": mobile_numbers})
df.to_csv('mobile_number_collector_from_map_google.csv', index=False)
print("CSV file created successfully")

driver.quit()

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
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
# chrome_options.page_load_strategy = "none"
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Initialize the driver
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://glgassets.com/top-real-estate-company-in-dhaka-bangladesh/')
for i in range(1, 21):
    try:
        i = str(i)
        li_elements = driver.find_elements(By.XPATH, f"/html/body/div[1]/div[2]/div/div/ul[{i}]/li")
        company_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div[2]/div/div/h3[{i}]/span/strong").text
        name = re.sub(r"^\d+\.\s*", "", company_name)
        print(name,'--------------------------------')
        phone_number = None
        telephone_number = None
        tel_numbers = []
        for li in li_elements:
            text = li.text.strip()  
            if "Tel:" in text:
                # Extract everything after "Tel:"
                tel_numbers_text = text.split("Tel:")[1].strip()
            
                # Use regex to find all phone numbers
                phone_numbers = re.findall(r'(\+?\d{1,4}[-\s]?\(?\d{1,4}\)?[-\s]?\d{1,4}[-\s]?\d{1,4}[-\s]?\d*)', tel_numbers_text)
                if phone_numbers:
                    tel_numbers.extend(phone_numbers)

        for i in tel_numbers: print(i)
    except Exception as e:
        print(f"Error: {e}")

driver.quit()
from selenium import webdriver
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
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Initialize the driver
driver = webdriver.Chrome(options=chrome_options)
link = 'https://www.daraz.com.bd/products/c001-i347762802-s1703060973.html'
link = 'https://www.daraz.com.bd/products/lotto-4l-lotto-i273872893-s1248847224.html'
link = 'https://www.daraz.com.bd/products/m7171-i453299157-s2170345155.html'
link = 'https://www.google.com/maps'

driver.get(link)

searchfield = driver.find_element(By.XPATH, f'//*[@id="searchboxinput"]')
# searchfield = driver.find_element(By.XPATH, f'//*[@id="APjFqb"]')
searchfield.send_keys('laptop shop near me\n')
time.sleep(5)
scrollable_div = driver.find_element(By.XPATH, f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]')
last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)

while True:
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
    time.sleep(5) 
    new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
    if new_height == last_height: break
    last_height = new_height

print("Scroll done")



names = []
mobile_numbers = []


for i in range(3,202,2):
    c = str(i)
    try:
        name = driver.find_element(By.XPATH, f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[{c}]/div/div[2]/div[4]/div[1]/div/div/div[2]/div[1]/div[2]').text
        text = driver.find_element(By.XPATH, f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[{c}]/div/div[2]/div[4]/div[1]/div/div/div[2]/div[4]/div[2]/span[last()]').text.strip()
        num = num = re.sub(r'[-· ]', '', text)
        if num and num.isdigit():
            names.append(name)
            mobile_numbers.append(num)

    except:
        print("Error to find element")
        break

    

df = pd.DataFrame({"Name": names, "Mobile": mobile_numbers})
df.to_csv('phone_num_collect.csv', index=False)
print("CSV file created successfully")

driver.quit()


# /html/body/div[3]/div/div[12]/div[1]/div[2]/div/div/div[1]/div/div/div/div[1]/div[2]/div/div[1]/div[2]/div/h3/g-more-link/a/div
# /html/body/div[3]/div/div[12]/div[1]/div[2]/div/div/div[1]/div/div/div/div[1]/div[2]/div/div[1]/div[2]/div/h3/g-more-link
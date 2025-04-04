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
# chrome_options.page_load_strategy = "none"
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Initialize the driver
driver = webdriver.Chrome(options=chrome_options)
link = 'https://www.google.com/localservices/prolist?g2lbs=AAEPWCuxA2JS-O84PCpA0gZj6g7wtRx_Td5QKQq4pilXHAO2CTmp84GBeElab6Ev081OBF6Oa1KTJ4DfB16vSQ0iS63BjEEojg%3D%3D&hl=bn-BD&gl=bd&cs=1&ssta=1&oq=Top%2050%20real%20estate%20company%20in%20Bangladesh&src=2&sa=X&q=real%20estate%20company%20in%20Bangladesh&ved=2ahUKEwiq6tvRzr6MAxW604QAHQoOEXwQjdcJegQIABAF&scp=ChpnY2lkOnJlYWxfZXN0YXRlX2RldmVsb3BlchIAGgAqPuCmsOCmv-Cmr-CmvOCnh-CmsiDgpo_gprjgp43gpp_gp4fgpp8g4Kah4KeH4Kat4KeH4Kay4Kaq4Ka-4Kaw&slp=MgBAAVIECAIgAIgBAJoBBgoCFxkQAA%3D%3D'
driver.get(link)

text = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[1]/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[3]').text
first_number = re.search(r"\d+", text).group()
pages = int(first_number)

# while True:
scrollable_div = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[1]/div/div[3]/div/div/div[1]/div[3]')
# driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
# ele = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[2]/div/div/button/span')
flag = False
namelist = []
phonelist = []

track = 1
while True:
# for i in range(3):
    print('tracking page: ', track)
    track = track + 1
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
    for j in range(1,40,2):
        c=str(j)
        phone = None
        try:
            name = driver.find_element(By.XPATH, f'//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[1]/c-wiz/div/div[{c}]/div[1]/div/div/div/div[2]/div[1]/div').text
            # print(name)
            namelist.append(name)
        except:
            continue

        try:
            text = driver.find_element(By.XPATH, f'//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[1]/c-wiz/div/div[{c}]/div[1]/div/div/div/div[2]/div[3]/span[last()]').text
            # print(text)
            if re.fullmatch(r'[0-9\-]+', text):
                phone = text.replace('-', '')
        except:
            print("no phone number")
        phonelist.append(phone)
        

    # Go to next pages
    time.sleep(2)
    try:
        button = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[2]/div[2]/div/button/span')
        driver.execute_script("arguments[0].click();", button)
    except:
        if flag:
            print("All pages are visited.")
            break;
        button = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[2]/div/div/button/span')
        driver.execute_script("arguments[0].click();", button)
        flag = True

    time.sleep(2)


df = pd.DataFrame({'Name': namelist, 'Phone': phonelist})
df.to_excel('real_estate_companies.xlsx', index=False)
driver.quit()
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
link = 'https://www.google.com/search?q=laptop+shop+near+mirpur%2C+dhaka&sca_esv=cbf74057595eaae5&biw=1920&bih=961&tbm=lcl&sxsrf=AHTn8zr4ff0QJNTwR33vpZTS4xBpTn5tcA%3A1743862643088&ei=czvxZ4aIBcqb4-EP34mg2Ak&oq=laptop+shop+near+mirpur&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhdsYXB0b3Agc2hvcCBuZWFyIG1pcnB1cioCCAAyBBAjGCcyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYogQYiQVI2CVQtAxYthdwAngAkAEBmAHzAqAB0hCqAQcwLjEuNS4yuAEByAEA-AEBmAIJoAKHD8ICChAAGIAEGEMYigXCAgUQABiABMICBxAAGIAEGA2YAwCIBgGSBwcyLjAuNS4yoAf3M7IHBTItNS4yuAf2Dg&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[23.8275129,90.3801258],[23.775847799999998,90.3629698]];start:0'
driver.get(link)
time.sleep(5)

names = []
mobile_numbers = []
count = 0
page = 20

while True:
    print('scripping page', page)
    for i in range(1, 21):
        c = str(i*2)
        try:
            name = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[7]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{c}]/div[2]/div/div/a[1]/div/div/div[1]/span').text
            phone = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[7]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[3]/div[{c}]/div[2]/div/div/a[1]/div/div/div[4]').text

            match = re.findall(r'[\d\-\+]+', phone)[-1]
            mobile_number = match.replace('-', '')
            
            if mobile_number and len(mobile_number) > 3:
                names.append(name)
                mobile_numbers.append(mobile_number)
                count += 1
                if count >= 100:
                    break
            #     print(f"Name: {name}, Mobile Number: {mobile_number}")

        except:
            print("Error to find element")

    if count >= 100:
        break
        
    link = f'https://www.google.com/search?q=laptop+shop+near+mirpur%2C+dhaka&sca_esv=cbf74057595eaae5&biw=1920&bih=961&tbm=lcl&sxsrf=AHTn8zr4ff0QJNTwR33vpZTS4xBpTn5tcA%3A1743862643088&ei=czvxZ4aIBcqb4-EP34mg2Ak&oq=laptop+shop+near+mirpur&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhdsYXB0b3Agc2hvcCBuZWFyIG1pcnB1cioCCAAyBBAjGCcyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYogQYiQVI2CVQtAxYthdwAngAkAEBmAHzAqAB0hCqAQcwLjEuNS4yuAEByAEA-AEBmAIJoAKHD8ICChAAGIAEGEMYigXCAgUQABiABMICBxAAGIAEGA2YAwCIBgGSBwcyLjAuNS4yoAf3M7IHBTItNS4yuAf2Dg&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[23.8275129,90.3801258],[23.775847799999998,90.3629698]];start:{page}'
    page += 20
    driver.get(link)
    time.sleep(5)

df = pd.DataFrame({"Name": names, "Mobile": mobile_numbers})
df.to_csv('laptop_shop_near_me.csv', index=False)
print("CSV file created successfully")

driver.quit()

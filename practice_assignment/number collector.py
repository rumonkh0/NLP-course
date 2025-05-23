from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
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
query = 'real estate company in bangladesh'
# query = input("Enter your search term:  ")
link = f"https://www.google.com/search?tbm=lcl&q={query.replace(' ', '+')}&hl=en"
driver.get(link)
wait = WebDriverWait(driver, 5)
time.sleep(4)

names = []
mobile_numbers = []
addresses = []
websites = []
count = 0
page = 0
total = 100
while True:
    page += 1
    print('scripping page-------------------------------------', page)
    initial_text = "init"
    for i in range(1, 21):
        # print(i)
        c = str(i*2)
        try:
            ele = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[7]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div{ '/div' if page != 1 else '' }/div[1]/div[3]/div[{c}]/div[2]/div/div/a[1]/div/div/div[1]/span')
            name = ele.text                                                  
            # print(name)
            add = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[7]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div{ '/div' if page != 1 else '' }/div[1]/div[3]/div[{c}]/div[2]/div/div/a[1]/div/div/div[3]').text
            # print(add)                            
            driver.execute_script("arguments[0].click();", ele)
            if i == 1: time.sleep(2)
            try:
                # wait.until(lambda driver: driver.find_element(By.XPATH, '//*[@data-attrid="kc:/local:alt phone"]').text != initial_text)
                # print("checked<<<<<<<")
                address, website = None, None
                try:
                    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div[7]/div[2]/div/div[2]/div')))
                except Exception as e:
                    print(e)
                # print('waited for parent------------')
                try:
                    element = driver.find_element(By.XPATH, '//*[@data-attrid="kc:/local:alt phone"]')
                except:
                    pass
                try:
                     address = driver.find_element(By.XPATH, '//*[@data-attrid="kc:/location/location:address"]').text
                     address = address.split(':', 1)[1].strip()
                except:
                    pass
                try:
                     website = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[7]/div[2]/div/div[2]/div/div/async-local-kp/div/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[4]/c-wiz/div/div/div[1]/a').get_attribute('href')
                except:
                    pass
                # print("checking visibility..........")
                # wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@data-attrid="kc:/local:alt phone"]')))
                # print('ele->>>>',element.text)
                # phone_span = target_element = element.find_element(By.XPATH, './div/div/span[2]/span/a/span')
                phone_number = re.sub(r'\D', '', element.text)
                initial_text = element.text
                mobile_numbers.append(phone_number)
                names.append(name)      
                addresses.append(address) 
                websites.append(website)  
                count += 1
                if count >= total:
                    break
            except Exception as e:
                 print("no mobile number%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>%")
            
            close = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[7]/div[2]/div/div[2]/div/div/div')
            driver.execute_script("arguments[0].click();", close)
        except Exception as e:
            print("Error to find element")
    if count >= total:
            print("Reached the total count. Creating csv file...")
            break   
    # input()
    try:
        next_button = driver.find_element(By.XPATH, '//*[@id="pnnext"]/span[2]')
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(3)  # Wait for the next page to load
    except Exception as e:
        print("Next button not found. Creating csv")
        break

print("creating csv file")
df = pd.DataFrame({"Name": names, "Mobile": mobile_numbers, "website": websites, "address": addresses})
df.to_csv('resturant.csv', index=False)
print("CSV file created successfully")

driver.quit()
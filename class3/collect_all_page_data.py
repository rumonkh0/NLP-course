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
chrome_options.page_load_strategy = "none"
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Initialize the driver
driver = webdriver.Chrome(options=chrome_options)

print("Loading page 1...")
driver.get('https://www.daraz.com.bd/catalog/?q=oven')

def scroll_page():
    time.sleep(8)
    total_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(1, total_height, 100):
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(0.1) 
    time.sleep(3)

scroll_page()

# Get total items (with error handling)
try:
    totalEleText = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[1]/div/div[1]/div/div/span[1]').text
    totalele = int(re.findall(r'\d+', totalEleText)[0])
    pages = math.ceil(totalele / 40)
    lastpageelements = totalele - (pages-1) * 40
    pages=1
except:
    print("Couldn't find total items element, defaulting to 1 page")
    pages = 1
    lastpageelements = 40

textlist = []
imagelinks = []  
links = []
pricelist = []
skulist = []
itemIds = []

for page in range(1, pages+1):
    if not page == 1:
        print(f'Loading page: {page}')
        driver.get(f'https://www.daraz.com.bd/catalog/?page={page}&q=oven')
        scroll_page()
    
    print(f'Scraping page: {page}')
    productPerPage = 40
    if page == pages:
        productPerPage = lastpageelements
    
    for i in range(1, productPerPage+1):
        try:
            ele = str(i)
            txt = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div[{ele}]/div/div/div[2]/div[2]/a').text
            img = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div[{ele}]/div/div/div[1]/div/a/div/img').get_attribute('src')
            link = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div[{ele}]/div/div/div[1]/div/a').get_attribute('href')
            sku = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div[{ele}]').get_attribute('data-sku-simple')
            itemId = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div[{ele}]').get_attribute('data-item-id')
            price = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div[{ele}]/div/div/div[2]/div[3]/span').text
            price = re.sub(r'\D', '', price)
            textlist.append(txt)
            imagelinks.append(img)
            links.append(link)
            skulist.append(sku)
            itemIds.append(itemId)
            pricelist.append(price)
        except:
            print(f"Error scraping product {i} on page {page}")
            continue

# Save to CSV
df = pd.DataFrame({
    "Title": textlist,
    "Image Link": imagelinks,
    "Product Link": links,
    "Price": pricelist,
    "SKU": skulist,
    "Item ID": itemIds,
})

df.to_csv("daraz_products_oven.csv", index=False)
print(f"Saved {len(df)} products to daraz_products_oven.csv")

driver.quit()
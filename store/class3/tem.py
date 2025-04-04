from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import math
import re
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.page_load_strategy = "none"

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1920, 1080)  # Set custom size

print("Loading page 1...")
driver.get('https://www.daraz.com.bd/catalog/?spm=a2a0e.tm80335411.search.d_go&q=men%20glass')
time.sleep(5)

# Define scroll steps
scroll_height = driver.execute_script("return document.body.scrollHeight")
scroll_steps = 50  # Number of pixels per step
scroll_delay = 5 / (scroll_height // scroll_steps)  # Delay per step

current_scroll = 0

while current_scroll < scroll_height:
    driver.execute_script(f"window.scrollBy(0, {scroll_steps});")
    current_scroll += scroll_steps
    time.sleep(scroll_delay)  
    
current_scroll = 0
time.sleep(5)


# Get the total items 
totalEleText = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[1]/div/div[1]/div/div/span[1]').text
totalele = int(re.findall(r'\d+', totalEleText)[0])
pages = math.ceil(totalele / 40)
lastpageelements = totalele - (pages-1) * 40

textlist = []
imagelinks = []  
links = []


for page in range(1, pages+1):
    if not page == 1:
        print(f'Loading page: {page}................................................................')
        p = str(page)
        driver.get(f'https://www.daraz.com.bd/catalog/?page={p}&q=men%20glass&spm=a2a0e.tm80335411.search.d_go')
        time.sleep(5)
        while current_scroll < scroll_height:
            driver.execute_script(f"window.scrollBy(0, {scroll_steps});")
            current_scroll += scroll_steps
            time.sleep(scroll_delay)  
        current_scroll = 0
        # Wait for elements to be present
        time.sleep(5)
    print(f'Scrappinng page: {page}')
    productPerPage = 40
    if page == pages:
        productPerPage = lastpageelements
    for i in range(1,productPerPage+1):
        ele = str(i)
        # print(f'page: {page} -> Producet {ele}')
        txt = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div[{ele}]/div/div/div[2]/div[2]/a').text
        img = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div[{ele}]/div/div/div[1]/div/a/div/img').get_attribute('src')
        link = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div[{ele}]/div/div/div[1]/div/a').get_attribute('href')
        textlist.append(txt)
        imagelinks.append(img)
        links.append(link)
    
    time.sleep(1)



# print('--------------------------------titles--------------------------------')
# for text in textlist:
#     print(text)
# print('--------------------------------imagelinks--------------------------------')
# for image in imagelinks:
#     print(image)
# print('--------------------------------links--------------------------------')
# for link in links:
#     print(link)

# Create a DataFrame
df = pd.DataFrame({
    "Text": textlist,
    "Image Link": imagelinks,
    "Page Link": links
})

# Save to CSV
df.to_csv("./output2.csv", index=False)
print('scripts complete and saved to output.csv')

# driver.quit()
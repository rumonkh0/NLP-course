import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

df = pd.read_excel("go.xlsx")  

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)


form_url = "https://forms.gle/nDGFxFzBszcasvHK9"
driver.get(form_url)
time.sleep(1)
for i, row in df.iterrows():
    inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
    
    inputs[0].send_keys(str(row['Name'])) 
    inputs[1].send_keys(str(row['Address'])) 

    # Click Submit
    driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span").click()
    print(f'from {i+1} done successfully')
    time.sleep(2)

    driver.get(form_url)
    time.sleep(1)

driver.quit()

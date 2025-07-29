from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

import time
from datetime import datetime

URL = "http://app55.nu.edu.bd/nu-web/applicantLogin.action?degreeName=Honours"
INTERVAL = 1  # seconds between retries

start_time = time.time()
attempt = 1
print("two")

driver = webdriver.Chrome()
print('one')
print(f"⏳ Starting to check {URL}...")

while True:
    try:
        print(f"Attempt {attempt}: Loading {URL}...")
        driver.get(URL)

        # Wait for title or some known element
        if "Applicant Login" in driver.title or "Application ID" in driver.page_source:
            end_time = time.time()
            elapsed = int(end_time - start_time)
            print(f"✅ Site loaded successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"🕒 Time elapsed: {elapsed} seconds (~{elapsed // 60} minutes)")

            with open("nu_selenium_log.txt", "a") as log:
                log.write(f"[{datetime.now()}] Site became available after {elapsed} seconds\n")
            break

    except:
        print(f"❌ Error loading page: ")
    
    print(f"Retrying in {INTERVAL} seconds...\n")
    time.sleep(INTERVAL)
    attempt += 1

time.sleep(40000)
driver.quit()

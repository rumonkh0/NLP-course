### **webscrapping**

selenium
puputter
cypress
playwrite
beautiful soup

### Locator type   // This is the valuable topics for mastering webscripping

xpath

# RAF

#driver.set\_page\_load\_timeout(60)  # Set page load timeout to 60 seconds


colab setup


from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import math
import re
import time
import os

# Setup ChromeDriver for Colab

!apt-get update
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
os.environ['PATH'] += os.pathsep + '/usr/bin/chromedriver'

# Set up Chrome options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Initialize the driver

driver = webdriver.Chrome(options=chrome_options)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Create Chrome options /home/rumon/.config/google-chrome
options = Options()
# Set to your real user data directory and profile name
options.add_argument("--user-data-dir=/home/rumon/.config/google-chrome")
options.add_argument("--profile-directory=Default")  # Or "Profile 1", "Profile 2", etc.

# Optional: headless mode OFF so you can see what's happening
# options.add_argument("--headless")

# Start Chrome with your real profile
driver = webdriver.Chrome(options=options)

# Open the website where you're logged in
driver.get("https://chat.deepseek.com/")

time.sleep(10)
driver.quit()


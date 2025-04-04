from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up the Chrome driver
driver = webdriver.Chrome()

# Open the URL
driver.get('https://www.rokomari.com/search?affId=oMKaMO69Or0K6kM&affs=33842&cma=604800&gad_source=1&gclid=CjwKCAjwwLO_BhB2EiwAx2e-31PNzkVqRRnogZbyeCM9V9u6B1K6c3wjg75LpviHxrh4LeagLbQVIRoC-NwQAvD_BwE&term=science&search_type=ALL&page=1')

driver.maximize_window() 

# scroll to bottom for image loading
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")                    

textlist = []
imagelinks = []  
links = []
               
for i in range(1 , 61):
    ele = str(i)
    text = driver.find_element(By.XPATH, f"/html/body/div[7]/div/div/div/section[2]/div[2]/div/div[{ele}]/div/a/div[2]/h4").text
    image = driver.find_element(By.XPATH, f"/html/body/div[7]/div/div/div/section[2]/div[2]/div/div[{ele}]/div/a/div[1]/img").get_attribute('src')
    link = driver.find_element(By.XPATH, f"/html/body/div[7]/div/div/div/section[2]/div[2]/div/div[{ele}]/div/a").get_attribute('href')
    textlist.append(text)
    imagelinks.append(image)
    links.append(link)


print('--------------------------------titles--------------------------------')
for text in textlist:
    print(text)
print()
print('--------------------------------imagelinks--------------------------------')
for image in imagelinks:
    print(image)
print('--------------------------------links--------------------------------')
for link in links:
    print(link)

      
driver.quit()

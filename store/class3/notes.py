# smooth scroll
driver.execute_script("""
    arguments[0].scrollTo({
        top: arguments[0].scrollHeight,
        behavior: 'smooth'
    })
""", scrollable_div)

# gragually scroll
scrollable_div = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[1]/div[3]')
last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)

while True:
    # Scroll down by 500 pixels
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
    time.sleep(1)  # Wait for content to load
    
    # Get new scroll height
    new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
    
    # Check if we've reached the bottom
    if new_height == last_height:
        break
    last_height = new_height

#click_button
    driver.execute_script("arguments[0].click();", button)
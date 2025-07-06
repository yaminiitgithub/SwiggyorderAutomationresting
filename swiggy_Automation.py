from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Screenshot helper
def take_screenshot(driver, name):
    path = os.path.join(os.getcwd(), f"{name}.png")
    driver.save_screenshot(path)

# Setup
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)
driver.maximize_window()

# Step 1: Open Swiggy
driver.get("https://www.swiggy.com/")
print("Title:", driver.title)
print("URL:", driver.current_url)

# Click Login
wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Login']"))).click()
time.sleep(2)

# Enter phone number
phone_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='mobile']")))
phone_input.send_keys("YOUR_PHONE_NUMBER")

print("Waiting for manual OTP entry...")
time.sleep(25)  # Manually enter OTP

# Step 2: Enter location
location_input = wait.until(EC.presence_of_element_located((By.ID, "location")))
location_input.send_keys("Bengaluru")
time.sleep(2)
location_input.send_keys(Keys.ARROW_DOWN)
location_input.send_keys(Keys.ENTER)
time.sleep(4)

# Step 3: Search restaurant
search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'Search for restaurants')]")))
search_box.send_keys("Domino's Pizza")
search_box.send_keys(Keys.ENTER)

# Click first restaurant
time.sleep(3)
restaurant = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'_1HEuF')])[1]")))
restaurant_name = restaurant.text
restaurant.click()
print("Restaurant:", restaurant_name)

# Step 4: Add second food item
time.sleep(4)
food_item = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[contains(@class,'styles_itemName')])[2]"))).text
print("Food item:", food_item)

add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[text()='ADD'])[2]")))
add_btn.click()
time.sleep(2)

take_screenshot(driver, "after_adding_item")

# Step 5: View cart
view_cart = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='View Cart']")))
view_cart.click()
time.sleep(3)

# Step 6: Increase quantity
plus_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'_2AMGo')]/div[3]")))
plus_btn.click()
time.sleep(1)

take_screenshot(driver, "after_increase_quantity")

# Step 7: Enter address
add_address_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Add New Address']")))
add_address_btn.click()
time.sleep(2)

wait.until(EC.presence_of_element_located((By.NAME, "house"))).send_keys("Flat 101, Maple Apartments")
driver.find_element(By.NAME, "landmark").send_keys("Near Park")
driver.find_element(By.XPATH, "//div[text()='Home']").click()
driver.find_element(By.XPATH, "//div[text()='Save Address & Proceed']").click()

time.sleep(3)
take_screenshot(driver, "after_address_entry")

# Step 8: Proceed to payment
proceed_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Proceed to pay']")))
proceed_btn.click()

time.sleep(5)
take_screenshot(driver, "after_proceed_to_pay")

# Step 9: Print cart total
try:
    total_element = driver.find_element(By.XPATH, "//div[contains(@class,'_3L1X9')]")
    print("Cart Total:", total_element.text)
except:
    print("Cart total not found.")

# Finish
driver.quit() 

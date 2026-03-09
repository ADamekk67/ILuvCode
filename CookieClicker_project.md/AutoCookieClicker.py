from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyautogui
from pynput.keyboard import Listener, KeyCode

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://orteil.dashnet.org/cookieclicker/")
# Wait for the page to load
time.sleep(2)
# Select English language
try:
    english_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'English')]")))
    english_button.click()
    time.sleep(1)
except:
    pass  # If already selected or not present, continue

# Try to dismiss cookie consent dialog
try:
    # Look for common consent buttons
    consent_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Agree') or contains(text(), 'OK')]")
    if consent_buttons:
        consent_buttons[0].click()
        time.sleep(1)
except:
    pass  # If no consent dialog, continue

# Wait for the big cookie to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "bigCookie")))
cookie = driver.find_element(By.ID, "bigCookie")

# Get the position of the big cookie on screen
window_pos = driver.get_window_position()
element_rect = cookie.rect
click_x = window_pos['x'] + element_rect['x'] + element_rect['width'] / 2
click_y = window_pos['y'] + element_rect['y'] + element_rect['height'] / 2

print("Press 'K' to click the cookie 100 times...")

def on_press(key):
    if key == KeyCode.from_char('k'):
        print("Starting 100 clicks...")
        for _ in range(100):
            pyautogui.click(click_x, click_y)
            time.sleep(0.1)
        print("Done!")
        return False  # Stop listener

with Listener(on_press=on_press) as listener:
    listener.join()

print("Script finished.")

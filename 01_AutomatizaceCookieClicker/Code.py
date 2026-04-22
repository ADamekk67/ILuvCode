import pyautogui # mysss
import time
import keyboard # Input
import threading # Multithreading
###


def click_loop():
    global AutoClicker, RunMain
    while RunMain:
        if AutoClicker:
            pyautogui.moveTo(BigCookieCoords)
            pyautogui.click()
        time.sleep(ClickTime)

def keyboard_loop():
    global AutoClicker, RunMain
    while RunMain:
        if keyboard.is_pressed('k'):
    
            AutoClicker = not AutoClicker
            print("\n Toggled AutoClicker to", AutoClicker)
            time.sleep(0.1)  # Debounce

        if keyboard.is_pressed('0'):

            AutoClicker = False
            print("\n More options:")
            print("  - Press e to exit")
            print("  - Press 1 to AutoUpgrade")

            if keyboard.is_pressed('e'):
                print("Exiting program.")
                RunMain = False
                break
           
           
    
        time.sleep(0.1)
        

print("\n Press 0 for options")
AutoClicker = False
RunMain = True


# Adjustable settings
ClickTime = 0.05 # Time between clicks in seconds
BigCookieCoords = (250, 500) # Placeholder for big cookie coordinates
TotalCookiesCoords = (300, 100) # Placeholder for total cookies coordinates
# Start threads
threading.Thread(target=click_loop, daemon=True).start()
keyboard_loop()  # Run keyboard monitoring in main thread
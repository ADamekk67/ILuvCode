import pyautogui # GUI automation
import time # Time management
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
            print("  - Press 1 to set click time")
            print("  - Press 2 to set upgrade coordinates")
            print("  - Press 3 to set total cookies coordinates")

            if keyboard.is_pressed('e'):
                print("Exiting program.")
                RunMain = False
                break
            elif keyboard.is_pressed('1'):
                print("1")
            elif keyboard.is_pressed('2'):
                print("2")
            elif keyboard.is_pressed('3'):
                print("Press x to set Total Cookies coordinates for x")
                while WFI:
                    WFI = True
                    if keyboard.is_pressed('x'):
                        TotalCookiesCoords = pyautogui.position()
                        print("Total Cookies coordinates set to", TotalCookiesCoords)
                        break
                print("Press y to set Total Cookies coordinates for y")
                while True:
                    if keyboard.is_pressed('y'):
                        TotalCookiesCoords = pyautogui.position()
                        print("Total Cookies coordinates set to", TotalCookiesCoords)
                        break

            time.sleep(0.1) # Debounce

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
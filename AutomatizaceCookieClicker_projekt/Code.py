import pyautogui
import time
import keyboard



print("Running in 5 seconds...")
time.sleep(5)  # Wait for 5 seconds before starting the clicks
AutoClicker = True
RunMain = True
print("Start")
while RunMain:
    
    if keyboard.is_pressed('8'):
        AutoClicker = not AutoClicker # Toggle the Stop variable when spacebar is pressed
        print("Toggled AutoClicker to", AutoClicker)  # Optional: Print the current state of AutoClicker
    if keyboard.is_pressed('7'):
        print("Exiting program.")
        RunMain = False

    if AutoClicker:
        time.sleep(1) 
        pyautogui.click()
    
    
        
  
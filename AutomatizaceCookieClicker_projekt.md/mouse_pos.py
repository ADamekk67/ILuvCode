import pyautogui
import keyboard
import time

print("Press '9' on the numpad to print current mouse coordinates. Press 'q' to quit.")

while True:
    if keyboard.is_pressed('9'):  # Numpad 9 (ensure Num Lock is on)
        x, y = pyautogui.position()
        print(f"Mouse coordinates: ({x}, {y})")
        time.sleep(0.2)  # Debounce to prevent multiple prints
    if keyboard.is_pressed('q'):
        print("Exiting.")
        break
    time.sleep(0.1)
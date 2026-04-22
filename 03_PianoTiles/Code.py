import win32api, win32con
import time
import keyboard
import pyautogui

Tile1Pos = (716, 400)
Tile2Pos = (872, 400)
Tile3Pos = (1034, 400)
Tile4Pos = (1178, 400)

print("Press 'e' to stop the program.")
def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)  # Short delay to simulate a click
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

while keyboard.is_pressed('e') == False:
    
    if pyautogui.pixel(716, 400) [0] == 0: # Is black?
        click(716, 400)
    if pyautogui.pixel(872, 400) [0] == 0: # Is black?
        click(872, 400)
    if pyautogui.pixel(1034, 400) [0] == 0: # Is black?
        click(1034, 400)
    if pyautogui.pixel(1178, 400) [0] == 0: # Is black?
        click(1178, 400)

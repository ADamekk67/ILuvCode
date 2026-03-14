# Cookie Clicker Automation Script

This Python script automates clicking in the Cookie Clicker game using the `pyautogui` library.

## Features

- Automatically clicks every second to generate cookies.
- Toggle auto-clicking on/off by pressing the '8' key.
- Exit the program by pressing the '7' key.
- Starts after a 5-second countdown to allow switching to the game window.

## Requirements

- Python 3.x
- `pyautogui` library: Install with `pip install pyautogui`
- `keyboard` library: Install with `pip install keyboard`

## Usage

1. Open Cookie Clicker in your browser.
2. Run the script: `python Code.py`
3. Switch to the game window within 5 seconds.
4. Use '8' to pause/resume clicking, '7' to stop the script.

**Note:** Ensure the game is in focus for the clicks to register. The script simulates mouse clicks at the current cursor position.

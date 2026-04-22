# Piano Tiles Bot

This project contains a Python script that automates playing the Piano Tiles game by detecting and clicking black tiles.

## Game Link
https://www.gamesgames.com/game/magic-piano-tiles

## Description

The `Code.py` script uses computer vision to detect black tiles in the Piano Tiles game and automatically clicks them. It works by:

1. Checking the color of pixels at four predefined positions corresponding to the four columns of tiles
2. If a pixel is black (indicating a tile that needs to be pressed), it simulates a mouse click at that position
3. The script runs continuously until the 'e' key is pressed

## Requirements

- Python 3.x
- Windows operating system (uses Windows-specific APIs)
- The Piano Tiles game running in a web browser

## Installation

1. Install the required Python packages:
   ```
   pip install pywin32 keyboard pyautogui
   ```

## Usage

1. Open the Piano Tiles game in your web browser at the link above
2. Position the game window so that the tile columns align with the hardcoded coordinates in the script
3. Run the script:
   ```
   python Code.py
   ```
4. The script will start monitoring the tile positions and clicking black tiles automatically
5. Press the 'e' key to stop the script

## Configuration

The tile positions are currently hardcoded for a specific screen resolution and window position:

- Tile 1: (716, 400)
- Tile 2: (872, 400)
- Tile 3: (1034, 400)
- Tile 4: (1178, 400)

If the clicks are not registering correctly, you may need to adjust these coordinates to match your screen setup. You can use tools like the included `mouse_pos.py` script to find the correct positions.

## Note

This script is for educational purposes only. Automated gameplay may violate the terms of service of some games.
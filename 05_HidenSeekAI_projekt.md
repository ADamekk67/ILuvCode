# Hide and Seek AI

## Overview

This project contains a simple hide-and-seek simulation with two AI agents.
- The **Seeker** moves toward the **Hider**.
- The **Hider** moves away from the **Seeker**.
- No grid system is used; both agents move by fixed pixel steps inside the window.

## Project files

- `main.py` — main game script

## How it works

1. The window opens with a seeker and a hider in opposite corners.
2. Each step, the hider chooses a move that maximizes distance from the seeker.
3. The seeker chooses a move that minimizes distance to the hider.
4. The game ends when the seeker catches the hider.

## Controls

- Run the game with:

```bash
python main.py
```

- Press **R** to reset the game.
- Close the window to quit.

## Requirements

- Python 3.x
- `pygame`

## Installation

Install the required package with:

```bash
pip install pygame
```

## Notes

This version is a clean starting point for further AI improvements, such as:
- smarter hiding strategies
- multiple seekers/hiders
- adaptive learning behavior

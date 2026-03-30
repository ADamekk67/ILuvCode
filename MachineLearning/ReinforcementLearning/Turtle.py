import pygame
import json
pygame.init()

# Environment
Screen = 1000
ScreenSize = pygame.display.set_mode((1000, 1000))
BackgroundColor = (255, 255, 255)
GridColor = (0, 0, 0)
GRID_SIZE = 20
GRID_WIDTH = 1000 // GRID_SIZE
GRID_HEIGHT = 1000 // GRID_SIZE
# Text
TextFont = pygame.font.SysFont("Arial", 24)

# Turtle
TurtleSize = 50
TurtleColor = (0, 255, 0)

TurtleSpawnPos = (1000 // 2 - TurtleSize // 2 - 25, 1000 // 2 - TurtleSize // 2 - 25)  # Center of the screen
TurtlePosX = TurtleSpawnPos[0]
TurtlePosY = TurtleSpawnPos[1]

TurtleSpawn = True
MainLoop = True
# Turtle Properties
try:
    with open("DataSave.json", 'r') as f:
        LoadedData = json.load(f)
        CollectedData = {
            "EpisodeData": set(LoadedData.get("EpisodeData", []))  # Convert list back to set
        }
except FileNotFoundError:
    print("FileNotFound - Initializing new data") # creates new file if not found
    
    CollectedData = {
        "EpisodeData": set()  # Use set for unique positions
    }


while MainLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            MainLoop = False

            # Convert set to list for JSON serialization
            DataToSave = CollectedData.copy()
            DataToSave["EpisodeData"] = list(CollectedData["EpisodeData"])
            with open("DataSave.json", 'w') as f:
                json.dump(DataToSave, f, indent=4)
            
            break

    # Eploration and action selection logic would go here
    CollectedData["EpisodeData"].add(("X: " + str(TurtlePosX), "Y: " + str(TurtlePosY)))

    # Game logic and rendering would go here

    ScreenSize.fill(BackgroundColor)  # Fill background
    # Draw grid
    for i in range(1, GRID_SIZE):
        # Vertical lines
        pygame.draw.line(ScreenSize, GridColor, (i * GRID_WIDTH, 0), (i * GRID_WIDTH, 1000))
        # Horizontal lines
        pygame.draw.line(ScreenSize, GridColor, (0, i * GRID_HEIGHT), (1000, i * GRID_HEIGHT))
    # Draw text
    episode_text = TextFont.render(f"Episode: ", True, (0, 0, 0))
    reward_text = TextFont.render(f"Reward: ", True, (0, 0, 0))
    ScreenSize.blit(episode_text, (10, 10)) 
    ScreenSize.blit(reward_text, (10, 40))

    # Spawn turtle
    pygame.draw.rect(ScreenSize, TurtleColor, (TurtlePosX, TurtlePosY, TurtleSize, TurtleSize))    

    pygame.time.Clock().tick(60)  # Limit to 60 FPS
    pygame.display.flip()
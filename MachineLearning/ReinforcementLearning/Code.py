import pygame
import json
import random
import threading
pygame.init()

# Environment
Screen = 1000
ScreenSize = pygame.display.set_mode((1000, 1000))
BackgroundColor = (255, 255, 255)
GridColor = (0, 0, 0)
GRID_SIZE = 20
GRID_WIDTH = 1000 // GRID_SIZE
GRID_HEIGHT = 1000 // GRID_SIZE
# Unsafe position
UnsafeColor = (255, 0, 0)
UnsafeSize = 49

# Text
TextFont = pygame.font.SysFont("Arial", 24)

# Turtle
TurtleSize = 49
TurtleColor = (0, 255, 0)
TurtleSpawnPos = (1000 // 2 - TurtleSize // 2 - 25, 1000 // 2 - TurtleSize // 2 - 25)  # Center of the screen / Default spawn position
TurtlePosX = TurtleSpawnPos[0]
TurtlePosY = TurtleSpawnPos[1]
TurtleState = "Explore"
TurtleSpawn = True
MainLoop = True
# Turtle Properties
StepsTaken = 1
pressed = False
# Json file loading and creation logic
try:
    with open("DataSave.json", 'r') as f:
        LoadedData = json.load(f)
        CollectedData = {
            "Steps Taken Total": LoadedData.get("Steps Taken Total", 0),
            "Safe Positions": set(tuple(item) for item in LoadedData.get("Safe Positions", [])),
            "Unsafe Positions": set(tuple(item) for item in LoadedData.get("Unsafe Positions", [(0, 0)]))
        }
        print("Data loaded successfully")
except FileNotFoundError: # If not found, create new file
    print("FileNotFound - Initializing new data")
    
    CollectedData = {
        "Steps Taken Total": 0,
        "Safe Positions": set(),
        "Unsafe Positions": set()
    }

# Q-Learning Setup
Q_TABLE = {}  # Dictionary to store Q-values: (state, action) -> Q-value
ALPHA = 0.1  # Learning rate
GAMMA = 0.9  # Discount factor
EPSILON = 0.5  # Exploration rate
ACTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']
ACTION_STEPS = 50  # Movement step size


# Threading setup
render_lock = threading.Lock()
render_stop = threading.Event()


def get_state(x, y):
    # Turtle position
    return (x // GRID_WIDTH, y // GRID_HEIGHT)

def get_reward(state):
    """Calculate reward based on state"""
    if state in CollectedData["Unsafe Positions"]:
        return -10
    elif state in CollectedData["Safe Positions"]:
        return 1
    return 0

def epsilon_greedy(state):
    """Select action using epsilon-greedy policy"""
    if random.random() < EPSILON:
        return random.choice(ACTIONS)
    else:
        q_values = [Q_TABLE.get((state, a), 0) for a in ACTIONS]
        return ACTIONS[q_values.index(max(q_values))]

def get_next_position(x, y, action):
    """Calculate next position based on action"""
    if action == 'UP':
        return (x, max(1, y - ACTION_STEPS))
    elif action == 'DOWN':
        return (x, min(1000 - TurtleSize, y + ACTION_STEPS))
    elif action == 'LEFT':
        return (max(1, x - ACTION_STEPS), y)
    elif action == 'RIGHT':
        return (min(1000 - TurtleSize, x + ACTION_STEPS), y)
    return (x, y)

def render_thread():
    """Rendering loop running in a separate thread"""
    clock = pygame.time.Clock()
    while not render_stop.is_set():
        with render_lock:
            ScreenSize.fill(BackgroundColor)  # Fill
            # Draw grid
            for i in range(1, GRID_SIZE): # Grid (síť)
                # Vertical lines
                pygame.draw.line(ScreenSize, GridColor, (i * GRID_WIDTH, 0), (i * GRID_WIDTH, 1000))
                # Horizontal lines
                pygame.draw.line(ScreenSize, GridColor, (0, i * GRID_HEIGHT), (1000, i * GRID_HEIGHT))
            
            # Draw text
            Episode_text = TextFont.render(f"Current Position: ({TurtlePosX}, {TurtlePosY})", True, (0, 0, 0))
            ScreenSize.blit(Episode_text, (10, 10)) 
            Reward_text = TextFont.render(f"State: {TurtleState}", True, (0, 0, 0))
            ScreenSize.blit(Reward_text, (10, 40))
            Stepstaken_text = TextFont.render(f"Steps Taken: {StepsTaken}", True, (0, 0, 0))
            ScreenSize.blit(Stepstaken_text, (10, 70))
            # Spawn turtle
            pygame.draw.rect(ScreenSize, TurtleColor, (TurtlePosX, TurtlePosY, TurtleSize, TurtleSize))
            pygame.draw.rect(ScreenSize, UnsafeColor, (501, 101, UnsafeSize, UnsafeSize))
            pygame.display.flip()
        
        clock.tick(20)  # FPS Limiter

### Main Loop
# Start rendering thread
rendering_thread = threading.Thread(target=render_thread, daemon=True)
rendering_thread.start()

while MainLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            MainLoop = False
            render_stop.set()  # Stop rendering thread

            # Save data to JSON file
            DataToSave = CollectedData.copy()
            DataToSave["Safe Positions"] = list(CollectedData["Safe Positions"])
            DataToSave["Unsafe Positions"] = list(CollectedData["Unsafe Positions"])
            DataToSave["Steps Taken Total"] += StepsTaken
            with open("DataSave.json", 'w') as f:
                json.dump(DataToSave, f, indent=4)
            
            break

    # Q-Learning Logic
    current_state = get_state(TurtlePosX, TurtlePosY)
    
    if TurtleState == "Explore":
        # Select action using epsilon-greedy
        action = epsilon_greedy(current_state)
        
        # Get next position
        next_x, next_y = get_next_position(TurtlePosX, TurtlePosY, action)
        next_state = get_state(next_x, next_y)
        
        # Get reward
        Reward = get_reward(next_state)
        
        # Q-Learning update
        current_q = Q_TABLE.get((current_state, action), 0)
        max_next_q = max([Q_TABLE.get((next_state, a), 0) for a in ACTIONS])
        Q_TABLE[(current_state, action)] = current_q + ALPHA * (Reward + GAMMA * max_next_q - current_q)
        
        # Move turtle
        TurtlePosX = next_x
        TurtlePosY = next_y
        StepsTaken += 1
        
        # Track positions
        CollectedData["Safe Positions"].add((TurtlePosX, TurtlePosY))
    
    pygame.time.Clock().tick(20)

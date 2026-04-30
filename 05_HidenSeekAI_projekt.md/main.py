import pygame
import json
import random
import threading

import my_library

print("\n ====================================================================")
pygame.init()

# 1 AI turtle
# 2 AI damian

# ============================================================================
# ENVIRONMENT CONFIGURATION
# ============================================================================
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background_color = (255, 255, 255)

FPS = 120
# ============================================================================
# VISUAL ELEMENTS
# ============================================================================
text_font = pygame.font.SysFont("Arial", 24)

# Turtle properties (Bob the turtle :D )
HiderSize = 50
HiderColor = (0, 0, 255)
HiderX, HiderY = ((SCREEN_WIDTH // 2 - HiderSize // 2 - 25) - 1, (SCREEN_HEIGHT // 2 - HiderSize // 2 - 25) - 1) # Start location

# Damian properties
SeekerColor = (255, 0, 0)
SeekerSize = 50
SeekerX, SeekerY = ((SCREEN_WIDTH // 2 - SeekerSize // 2 - 25) - 1, (SCREEN_HEIGHT // 2 - SeekerSize // 2 - 25) - 1) # Start location

# ============================================================================
# GAME STATE
# ============================================================================
main_loop = True

# ============================================================================
# DATA LOADING
# ============================================================================

print("Loading MapLayout.json if it exists...")

try:
    with open("MapLayout.json", 'r') as f:
        map_data = json.load(f)
        map_layout = {
            
        }
        print("Map data loaded successfully")
except FileNotFoundError:
    print("MapLayout.json not found - No map data loaded")
    map_layout = {
        
    }


# ============================================================================
# Q-LEARNING CONFIGURATION
# ============================================================================
# Q-table stores learned knowledge: for each (state, action) pair, 
# it stores the expected future reward. Starts empty and builds as turtle learns.

try:
    with open("DataSave.json", 'r') as f:
        loaded_data = json.load(f)
    
    q_table = {
    eval(k): v for k, v in loaded_data.get("Q_Table", {}).items()
}
except FileNotFoundError:
    print("DataSave.json not found - Starting with empty Q-table")
    q_table = {}  

# Learning rate (alpha) controls how much new information overrides old knowledge.
# 0.1 means new experiences have 10% influence, old knowledge has 90% influence.
alpha = 0.2           # Learning rate (0-1): higher = learn faster but less stable

# Discount factor (gamma) determines how much we value future rewards vs immediate rewards.
# 0.9 means we care a lot about future outcomes, 0.0 means only immediate reward matters.
gamma = 0.4           # Discount factor (0-1): how much to value future rewards

# Exploration rate (epsilon) controls exploration vs exploitation balance.
# 0.5 means 50% random exploration, 50% using best known strategy.
# As the turtle learns, you may want to lower this to favor learned strategies.
epsilon = 1    # Exploration rate (0-1): probability of random action
# Epsilon decay parameters
epsilon_min = 0.2 # Minimum exploration rate
epsilon_decay = 0.999 # How much epsilon decreases each step

# Available directions the turtle can move in
MoveActions = ['UP', 'DOWN', 'LEFT', 'RIGHT']



# ============================================================================
# OTHER CONFIGURATION
# ============================================================================
render_lock = threading.Lock()
render_stop = threading.Event()

# Track previous state for repeated movement detection
previous_state = None
repeated_movement_penalty = -0.5  # Penalty for repeating movements

# ============================================================================
# GAME FUNCTIONS
# ============================================================================

def get_state(x, y):
    """Convert pixel coordinates to grid state."""
    return (x // grid_width, y // grid_height)


def get_reward(state):
    """Calculate reward based on current state."""
    if state in map_layout["Red Blocks"]:
        return red
    elif state in map_layout["Blue Blocks"]:
        return blue
    elif state in map_layout["Yellow Blocks"]:
        return yellow
    elif state in map_layout["Black Blocks"]:
        return black
    else:
        return white
    
def epsilon_greedy(state):
    """Select action using epsilon-greedy policy."""
    if random.random() < epsilon:
        return random.choice(MoveActions)
    else:
        q_values = [q_table.get((state, a), 0) for a in MoveActions]
        max_q = max(q_values)
        best_actions = [a for a in MoveActions if q_table.get((state, a), 0) == max_q]
        return random.choice(best_actions)

def get_next_position(x, y, action):
    """Calculate next position based on action."""
    # Calculate grid-aligned boundaries
    max_x = ((SCREEN_WIDTH // grid_width) - 1) * grid_width
    max_y = ((SCREEN_HEIGHT // grid_height) - 1) * grid_height
    
    if action == 'UP':
        return (x, max(0, y - action_steps))
    elif action == 'DOWN':
        return (x, min(max_y, y + action_steps))
    elif action == 'LEFT':
        return (max(0, x - action_steps), y)
    elif action == 'RIGHT':
        return (min(max_x, x + action_steps), y)
    return (x, y)

# ============================================================================
# RENDER LOOP
# ============================================================================

def render_thread():
    """Rendering loop running in a separate thread."""
    clock = pygame.time.Clock()
    while not render_stop.is_set():
        with render_lock:
            screen.fill(background_color)
            
            # Draw grid including border lines
            for i in range(0, grid_size + 1):
                # Vertical lines
                pygame.draw.line(screen, grid_color, (i * grid_width - 1, 0), 
                                (i * grid_width - 1, SCREEN_HEIGHT - 1))
                # Horizontal lines
                pygame.draw.line(screen, grid_color, (0, i * grid_height - 1), 
                                (SCREEN_WIDTH - 1, i * grid_height - 1))
            
            # Draw all Black blocks (walls)
            for black_grid_x, black_grid_y in map_layout.get("Black Blocks", []):
                black_pixel_x = black_grid_x * grid_width
                black_pixel_y = black_grid_y * grid_height
                pygame.draw.rect(screen, (0, 0, 0), 
                                (black_pixel_x, black_pixel_y, unsafe_size, unsafe_size))

            # Draw all Red blocks (unsafe blocks)
            for unsafe_grid_x, unsafe_grid_y in map_layout.get ("Red Blocks", []):
                unsafe_pixel_x = unsafe_grid_x * grid_width
                unsafe_pixel_y = unsafe_grid_y * grid_height
                pygame.draw.rect(screen, unsafe_color, 
                                (unsafe_pixel_x, unsafe_pixel_y, unsafe_size, unsafe_size))
            # Draw all blue blocks (small reward blocks)
            for blue_grid_x, blue_grid_y in map_layout.get("Blue Blocks", []):
                blue_pixel_x = blue_grid_x * grid_width
                blue_pixel_y = blue_grid_y * grid_height
                pygame.draw.rect(screen, (0, 0, 255), 
                                (blue_pixel_x, blue_pixel_y, unsafe_size, unsafe_size))
            # Draw all yellow blocks (big reward blocks)
            for yellow_grid_x, yellow_grid_y in map_layout.get("Yellow Blocks", []):
                yellow_pixel_x = yellow_grid_x * grid_width
                yellow_pixel_y = yellow_grid_y * grid_height
                pygame.draw.rect(screen, (255, 255, 0), 
                                (yellow_pixel_x, yellow_pixel_y, unsafe_size, unsafe_size))

            # Draw UI text
            position_text = text_font.render(
                f"Current Position: ({turtle_x}, {turtle_y})", True, (0, 0, 0))
            screen.blit(position_text, (10, 10))
            
            steps_text = text_font.render(
                f"Steps Taken: {steps_taken}", True, (0, 0, 0))
            screen.blit(steps_text, (10, 70))

            mode_text = text_font.render(
                f"Current Mode: {Mode}", True, (0, 0, 0))
            screen.blit(mode_text, (10, 130))

            pygame.draw.rect(screen, turtle_color, 
                            (turtle_x, turtle_y, turtle_size, turtle_size))
            
            pygame.display.flip()
        
        clock.tick(FPS)  # FPS


# ============================================================================
# MAIN LOOP
# ============================================================================

# Start rendering thread
rendering_thread = threading.Thread(target=render_thread, daemon=True)
rendering_thread.start()

while main_loop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_loop = False
            render_stop.set()

            # Save Q-table to JSON file
            q_table_to_save = {str(k): v for k, v in q_table.items()}
            data_to_save = {
                "Q_Table": q_table_to_save
            }
            with open("DataSave.json", 'w') as f:
                json.dump(data_to_save, f, indent=4)

            # Save map layout to JSON file
            map_data_to_save = {
            }
            with open("MapLayout.json", 'w') as f:
                json.dump(map_data_to_save, f, indent=4)
            break
        
# ========================================================================
# User Interaction/Input
# ========================================================================

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            pass        

# ========================================================================
# Q-LEARNING UPDATE
# ========================================================================
    
    # Get current state
    current_state = get_state(turtle_x, turtle_y)
    
    # Select action using epsilon-greedy policy
    action = epsilon_greedy(current_state)
    
    # Calculate next position
    next_x, next_y = get_next_position(turtle_x, turtle_y, action)
    next_state = get_state(next_x, next_y)
    
    # Get reward for next state
    reward = get_reward(next_state)

    # Update Q-table using Q-learning formula
    current_q = q_table.get((current_state, action), 0)
    max_next_q = max([q_table.get((next_state, a), 0) for a in actions])
    q_table[(current_state, action)] = current_q + alpha * (reward + gamma * max_next_q - current_q)
    
    # Decay epsilon over time to shift from exploration to exploitation
    epsilon = max(epsilon_min, epsilon * epsilon_decay)
    
    # Move turtle to next position
    turtle_x = next_x
    turtle_y = next_y
    steps_taken += 1
    
    # Track previous state for next iteration
    previous_state = current_state
    
    if printQ:
        print(f"Action: {action}, Reward: {reward}, New Q-value: {q_table[(current_state, action)]:.2f}, Epsilon: {epsilon:.3f}")
    
    # Track position as safe (using grid coordinates)
    current_grid_state = get_state(turtle_x, turtle_y)
    pygame.time.Clock().tick(FPS)

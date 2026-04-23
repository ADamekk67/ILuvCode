import pygame
import json
import random
import threading

import my_library

print("\n ====================================================================")
pygame.init()
# ============================================================================
# ENVIRONMENT CONFIGURATION
# ============================================================================
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background_color = (255, 255, 255)
grid_color = (0, 0, 0)
grid_size =  20
grid_width = SCREEN_WIDTH // grid_size
grid_height = SCREEN_HEIGHT // grid_size

FPS = 60
# ============================================================================
# VISUAL ELEMENTS
# ============================================================================
text_font = pygame.font.SysFont("Arial", 24)

# Turtle properties (Bob the turtle :D )
turtle_size = 49
turtle_color = (0, 255, 0)
steps_taken = 0
turtle_x, turtle_y = ((SCREEN_WIDTH // 2 - turtle_size // 2 - 25) - 1, (SCREEN_HEIGHT // 2 - turtle_size // 2 - 25) - 1)  
unsafe_color = (255, 0, 0)
unsafe_size = 49
unsafe_positions_count = 0
# ============================================================================
# GAME STATE
# ============================================================================
main_loop = True
printQ = True  # Set to True to print Q-learning details each step
# ============================================================================
# DATA COLLECTION
# ============================================================================

print("Loading MapLayout.json if they exist...")

try:
    with open("MapLayout.json", 'r') as f:
        map_data = json.load(f)
        map_layout = {
            "Unsafe Blocks": set(tuple(item) for item in map_data.get("Unsafe Blocks", []))
        }
        print("Map data loaded successfully")
except FileNotFoundError:
    print("MapLayout.json not found - No map data loaded")
    map_layout = {
        "Unsafe Blocks": set()
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
alpha = 0.1           # Learning rate (0-1): higher = learn faster but less stable

# Discount factor (gamma) determines how much we value future rewards vs immediate rewards.
# 0.9 means we care a lot about future outcomes, 0.0 means only immediate reward matters.
gamma = 0.9           # Discount factor (0-1): how much to value future rewards

# Exploration rate (epsilon) controls exploration vs exploitation balance.
# 0.5 means 50% random exploration, 50% using best known strategy.
# As the turtle learns, you may want to lower this to favor learned strategies.
epsilon = 0.2       # Exploration rate (0-1): probability of random action
# Epsilon decay parameters
epsilon_min = 0    # Minimum exploration rate
epsilon_decay = 0.999 # How much epsilon decreases each step

# Available directions the turtle can move in
actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

# Distance the turtle moves per action (in pixels).
# 50 pixels = 1 grid cell (since grid_width = grid_height = 50)
action_steps = 50     # Movement step size (pixels per action)

# Rewards for the turtle's actions: negative for unsafe positions, positive for safe positions.

penalty = 2 # Penalty for unsafe positions
safe = -1 # Reward for safe positions
gold = 10 # Reward for reaching the goal (if implemented)
# ============================================================================
# THREADING
# ============================================================================
render_lock = threading.Lock()
render_stop = threading.Event()



# ============================================================================
# GAME FUNCTIONS
# ============================================================================

def get_state(x, y):
    """Convert pixel coordinates to grid state."""
    return (x // grid_width, y // grid_height)


def pixel_to_grid_coords(mouse_x, mouse_y):
    """Convert mouse pixel coordinates to grid cell coordinates (top-left corner)."""
    grid_x = (mouse_x // grid_width) * grid_width
    grid_y = (mouse_y // grid_height) * grid_height
    return (grid_x, grid_y)


def get_reward(state):
    """Calculate reward based on current state."""
    if state in map_layout["Unsafe Blocks"]:
        return penalty
    else:
        return safe
    
def epsilon_greedy(state):
    """Select action using epsilon-greedy policy."""
    if random.random() < epsilon:
        return random.choice(actions)
    else:
        q_values = [q_table.get((state, a), 0) for a in actions]
        max_q = max(q_values)
        best_actions = [a for a in actions if q_table.get((state, a), 0) == max_q]
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
            
            # Draw all unsafe zones
            for unsafe_grid_x, unsafe_grid_y in map_layout.get("Unsafe Blocks", []):
                unsafe_pixel_x = unsafe_grid_x * grid_width
                unsafe_pixel_y = unsafe_grid_y * grid_height
                pygame.draw.rect(screen, unsafe_color, 
                                (unsafe_pixel_x, unsafe_pixel_y, unsafe_size, unsafe_size))

            # Draw UI text
            position_text = text_font.render(
                f"Current Position: ({turtle_x}, {turtle_y})", True, (0, 0, 0))
            screen.blit(position_text, (10, 10))
            
            steps_text = text_font.render(
                f"Steps Taken: {steps_taken}", True, (0, 0, 0))
            screen.blit(steps_text, (10, 70))
            
            epsilon_text = text_font.render(
                f"Epsilon: {epsilon:.3f}", True, (0, 0, 0))
            screen.blit(epsilon_text, (10, 110))

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
                "Unsafe Blocks": list(map_layout.get("Unsafe Blocks", []))
            }
            with open("MapLayout.json", 'w') as f:
                json.dump(map_data_to_save, f, indent=4)
            break
        
        # Handle mouse clicks to mark unsafe positions
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_x, mouse_y = event.pos
                grid_state = get_state(mouse_x, mouse_y)
                map_layout["Unsafe Blocks"].add(grid_state)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right click to remove unsafe block
                mouse_x, mouse_y = event.pos
                grid_state = get_state(mouse_x, mouse_y)
                map_layout["Unsafe Blocks"].discard(grid_state)

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
    if printQ:
        print(f"Action: {action}, Reward: {reward}, New Q-value: {q_table[(current_state, action)]:.2f}, Epsilon: {epsilon:.3f}")
    
    # Track position as safe (using grid coordinates)
    current_grid_state = get_state(turtle_x, turtle_y)
    pygame.time.Clock().tick(FPS)

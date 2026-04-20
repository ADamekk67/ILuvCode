import pygame
import json
import random
import threading

pygame.init()

# ============================================================================
# ENVIRONMENT CONFIGURATION
# ============================================================================
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background_color = (255, 255, 255)
grid_color = (0, 0, 0)
grid_size = 20
grid_width = SCREEN_WIDTH // grid_size
grid_height = SCREEN_HEIGHT // grid_size

# ============================================================================
# VISUAL ELEMENTS
# ============================================================================
text_font = pygame.font.SysFont("Arial", 24)

# Turtle properties
turtle_size = 49
turtle_color = (0, 255, 0)
turtle_spawn_pos = (SCREEN_WIDTH // 2 - turtle_size // 2 - 25, 
                    SCREEN_HEIGHT // 2 - turtle_size // 2 - 25)
turtle_x = turtle_spawn_pos[0]
turtle_y = turtle_spawn_pos[1]
steps_taken = 1

# Unsafe position
unsafe_color = (255, 0, 0)
unsafe_size = 49

# ============================================================================
# GAME STATE
# ============================================================================
main_loop = True
# ============================================================================
# DATA PERSISTENCE
# ============================================================================
try:
    with open("DataSave.json", 'r') as f:
        loaded_data = json.load(f)
        collected_data = {
            "Steps Taken Total": loaded_data.get("Steps Taken Total", 0),
            "Safe Positions": set(tuple(item) for item in loaded_data.get("Safe Positions", [])),
            "Unsafe Positions": set(tuple(item) for item in loaded_data.get("Unsafe Positions", [(0, 0)]))
        }
        print("Data loaded successfully")
except FileNotFoundError:
    print("FileNotFound - Initializing new data")
    collected_data = {
        "Steps Taken Total": 0,
        "Safe Positions": set(),
        "Unsafe Positions": set()
    }


# ============================================================================
# Q-LEARNING CONFIGURATION
# ============================================================================
q_table = {}          # Dictionary to store Q-values: (state, action) -> Q-value
alpha = 0.1           # Learning rate
gamma = 0.9           # Discount factor
epsilon = 0.5         # Exploration rate
actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
action_steps = 50     # Movement step size

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
    if state in collected_data["Unsafe Positions"]:
        return -10
    elif state in collected_data["Safe Positions"]:
        return 1
    return 0


def epsilon_greedy(state):
    """Select action using epsilon-greedy policy."""
    if random.random() < epsilon:
        return random.choice(actions)
    else:
        q_values = [q_table.get((state, a), 0) for a in actions]
        return actions[q_values.index(max(q_values))]


def get_next_position(x, y, action):
    """Calculate next position based on action."""
    if action == 'UP':
        return (x, max(1, y - action_steps))
    elif action == 'DOWN':
        return (x, min(SCREEN_HEIGHT - turtle_size, y + action_steps))
    elif action == 'LEFT':
        return (max(1, x - action_steps), y)
    elif action == 'RIGHT':
        return (min(SCREEN_WIDTH - turtle_size, x + action_steps), y)
    return (x, y)


def render_thread():
    """Rendering loop running in a separate thread."""
    clock = pygame.time.Clock()
    while not render_stop.is_set():
        with render_lock:
            screen.fill(background_color)
            
            # Draw grid
            for i in range(1, grid_size):
                # Vertical lines
                pygame.draw.line(screen, grid_color, (i * grid_width, 0), 
                                (i * grid_width, SCREEN_HEIGHT))
                # Horizontal lines
                pygame.draw.line(screen, grid_color, (0, i * grid_height), 
                                (SCREEN_WIDTH, i * grid_height))
            
            # Draw UI text
            position_text = text_font.render(
                f"Current Position: ({turtle_x}, {turtle_y})", True, (0, 0, 0))
            screen.blit(position_text, (10, 10))
            
            steps_text = text_font.render(
                f"Steps Taken: {steps_taken}", True, (0, 0, 0))
            screen.blit(steps_text, (10, 70))
            
            # Draw turtle
            pygame.draw.rect(screen, turtle_color, 
                            (turtle_x, turtle_y, turtle_size, turtle_size))
            
            # Draw all unsafe zones
            for unsafe_pos_x, unsafe_pos_y in collected_data["Unsafe Positions"]:
                pygame.draw.rect(screen, unsafe_color, 
                                (unsafe_pos_x, unsafe_pos_y, grid_width, grid_height))
            
            pygame.display.flip()
        
        clock.tick(20)  # 20 FPS


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
            
            # Save data to JSON file
            data_to_save = collected_data.copy()
            data_to_save["Safe Positions"] = list(collected_data["Safe Positions"])
            data_to_save["Unsafe Positions"] = list(collected_data["Unsafe Positions"])
            data_to_save["Steps Taken Total"] += steps_taken
            with open("DataSave.json", 'w') as f:
                json.dump(data_to_save, f, indent=4)
            break
        
        # Handle mouse clicks to mark unsafe positions
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_x, mouse_y = event.pos
                grid_x, grid_y = pixel_to_grid_coords(mouse_x, mouse_y)
                collected_data["Unsafe Positions"].add((grid_x, grid_y))
                print(f"Marked unsafe position: ({grid_x}, {grid_y})")
    
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
    
    # Move turtle to next position
    turtle_x = next_x
    turtle_y = next_y
    steps_taken += 1
    
    # Track position as safe
    collected_data["Safe Positions"].add((turtle_x, turtle_y))
    
    pygame.time.Clock().tick(20)

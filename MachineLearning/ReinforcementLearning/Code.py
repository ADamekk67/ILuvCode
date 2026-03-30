import pygame
import math
import random
from collections import defaultdict

pygame.init()

screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Reinforcement Learning")

TextFont = pygame.font.SysFont("Arial", 24)

# Bot
BotSize = 50
BotColor = (0, 255, 0)
BotX = 1920 // 2 - BotSize // 2
BotY = 1080 // 2 - BotSize // 2
BotSpeed = 5

# Rewards
TotalReward = 0

# RL parameters
epsilon = 0.1  # Exploration rate
alpha = 0.1    # Learning rate
gamma = 0.9    # Discount factor
actions = [(-BotSpeed, 0), (BotSpeed, 0), (0, -BotSpeed), (0, BotSpeed)]  # Left, Right, Up, Down
action_names = ["Left", "Right", "Up", "Down"]

# Q-table: state -> list of Q-values for each action
Q = defaultdict(lambda: [0.0] * 4)

# Grid for states
GRID_SIZE = 20
GRID_WIDTH = 1920 // GRID_SIZE
GRID_HEIGHT = 1080 // GRID_SIZE

def get_state(x, y):
    grid_x = min(x // GRID_WIDTH, GRID_SIZE - 1)
    grid_y = min(y // GRID_HEIGHT, GRID_SIZE - 1)
    return (grid_x, grid_y)

# Target
TargetSize = 30
TargetColor = (255, 0, 0)
TargetX = random.randint(0, 1920 - TargetSize)
TargetY = random.randint(0, 1080 - TargetSize)

MainLoop = True
clock = pygame.time.Clock()
episode = 0

while MainLoop:
    episode += 1
    BotX = 1920 // 2 - BotSize // 2
    BotY = 1080 // 2 - BotSize // 2
    TargetX = random.randint(0, 1920 - TargetSize)
    TargetY = random.randint(0, 1080 - TargetSize)
    episode_reward = 0
    steps = 0

    while True:  # Episode loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                MainLoop = False
                break

        if not MainLoop:
            break

        current_state = get_state(BotX, BotY)

        # Choose action: epsilon-greedy
        if random.random() < epsilon:
            action_idx = random.randint(0, 3)  # Explore
        else:
            action_idx = Q[current_state].index(max(Q[current_state]))  # Exploit

        dx, dy = actions[action_idx]

        # Calculate distance before move
        old_distance = math.hypot(BotX - TargetX, BotY - TargetY)

        # Apply movement
        new_BotX = BotX + dx
        new_BotY = BotY + dy

        # Keep bot within bounds
        new_BotX = max(0, min(1920 - BotSize, new_BotX))
        new_BotY = max(0, min(1080 - BotSize, new_BotY))

        # Calculate distance after move
        new_distance = math.hypot(new_BotX - TargetX, new_BotY - TargetY)

        # Reward: -0.01 per step, +0.1 if moving closer to target, +1 if target reached
        reward = -0.01
        if new_distance < old_distance:
            reward += 0.1  # Reward for moving closer
        done = False
        if abs(new_BotX - TargetX) < BotSpeed and abs(new_BotY - TargetY) < BotSpeed:
            reward += 1.0
            done = True

        new_state = get_state(new_BotX, new_BotY)

        # Update Q-value
        old_q = Q[current_state][action_idx]
        max_future_q = max(Q[new_state]) if not done else 0
        Q[current_state][action_idx] = old_q + alpha * (reward + gamma * max_future_q - old_q)

        # Update position
        BotX = new_BotX
        BotY = new_BotY
        episode_reward += reward
        steps += 1

        if done:
            TotalReward += episode_reward
            break

        # Redraw everything each frame
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, BotColor, (BotX, BotY, BotSize, BotSize))
        pygame.draw.rect(screen, TargetColor, (TargetX, TargetY, TargetSize, TargetSize))

        RewardText = TextFont.render(f"Episode: {episode} | Steps: {steps} | Total Reward: {TotalReward:.2f}", True, (255, 255, 255))
        screen.blit(RewardText, (10, 10))

        pygame.display.flip()
        clock.tick(60)

pygame.quit()

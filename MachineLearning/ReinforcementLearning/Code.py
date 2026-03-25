import pygame
import math
import random

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
CurrentReward = 0
PreviousReward = 0

# RL parameters
epsilon = 0.1  # Exploration rate
actions = [(-BotSpeed, 0), (BotSpeed, 0), (0, -BotSpeed), (0, BotSpeed)]  # Left, Right, Up, Down

# Target
TargetSize = 30
TargetColor = (255, 0, 0)
TargetX = random.randint(0, 1920 - TargetSize)
TargetY = random.randint(0, 1080 - TargetSize)

MainLoop = True
clock = pygame.time.Clock()

while MainLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            MainLoop = False

    # Bot makes decision: epsilon-greedy
    if random.random() < epsilon:
        # Explore: random action
        dx, dy = random.choice(actions)
    else:
        # Exploit: move towards target
        dx = 0
        dy = 0
        if BotX < TargetX:
            dx = BotSpeed
        elif BotX > TargetX:
            dx = -BotSpeed
        if BotY < TargetY:
            dy = BotSpeed
        elif BotY > TargetY:
            dy = -BotSpeed
    
    # Apply movement
    BotX += dx
    BotY += dy
    
    # Keep bot within bounds
    BotX = max(0, min(1920 - BotSize, BotX))
    BotY = max(0, min(1080 - BotSize, BotY))

    # Check target reached
    if abs(BotX - TargetX) < BotSpeed and abs(BotY - TargetY) < BotSpeed:
        PreviousReward = CurrentReward
        CurrentReward += 1
        TargetX = random.randint(0, 1920 - TargetSize)
        TargetY = random.randint(0, 1080 - TargetSize)

    # Redraw everything each frame
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, BotColor, (BotX, BotY, BotSize, BotSize))
    pygame.draw.rect(screen, TargetColor, (TargetX, TargetY, TargetSize, TargetSize))

    RewardText = TextFont.render(f"Current Reward: {CurrentReward} | Previous Reward: {PreviousReward}", True, (255, 255, 255))
    screen.blit(RewardText, (10, 10))

    pygame.display.flip()
    clock.tick(60)

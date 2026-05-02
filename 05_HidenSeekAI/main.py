import pygame
import random

# ---------------------------
# Configuration
# ---------------------------
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
STEP_SIZE = 40
FPS = 10

BACKGROUND_COLOR = (20, 20, 30)
SEEKER_COLOR = (220, 80, 80)
HIDER_COLOR = (80, 180, 220)
TEXT_COLOR = (230, 230, 230)

# ---------------------------
# Agent class
# ---------------------------

class Agent:
    def __init__(self, name, x, y, color):
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.size = 40

    def move(self, dx, dy):
        self.x = max(0, min(SCREEN_WIDTH - self.size, self.x + dx))
        self.y = max(0, min(SCREEN_HEIGHT - self.size, self.y + dy))

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self.color,
            pygame.Rect(self.x, self.y, self.size, self.size),
        )

    def distance_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


# ---------------------------
# Movement helpers
# ---------------------------

def get_actions():
    return [(-STEP_SIZE, 0), (STEP_SIZE, 0), (0, -STEP_SIZE), (0, STEP_SIZE)]


def seeker_move(seeker, hider):
    best_move = (0, 0)
    best_distance = float('inf')

    for dx, dy in get_actions():
        new_x = max(0, min(SCREEN_WIDTH - seeker.size, seeker.x + dx))
        new_y = max(0, min(SCREEN_HEIGHT - seeker.size, seeker.y + dy))
        distance = abs(new_x - hider.x) + abs(new_y - hider.y)

        if distance < best_distance:
            best_distance = distance
            best_move = (dx, dy)

    return best_move


def hider_move(hider, seeker):
    best_move = (0, 0)
    best_distance = -1

    for dx, dy in get_actions():
        new_x = max(0, min(SCREEN_WIDTH - hider.size, hider.x + dx))
        new_y = max(0, min(SCREEN_HEIGHT - hider.size, hider.y + dy))
        distance = abs(new_x - seeker.x) + abs(new_y - seeker.y)

        if distance > best_distance:
            best_distance = distance
            best_move = (dx, dy)

    return best_move


def render(screen, font, seeker, hider, steps, caught):
    screen.fill(BACKGROUND_COLOR)
    seeker.draw(screen)
    hider.draw(screen)

    status = 'Caught!' if caught else 'Running...'
    lines = [
        f'Seeker: ({seeker.x}, {seeker.y})',
        f'Hider: ({hider.x}, {hider.y})',
        f'Steps: {steps}',
        f'Status: {status}',
        'Press R to reset',
        'Close window to quit',
    ]

    for index, text in enumerate(lines):
        surface = font.render(text, True, TEXT_COLOR)
        screen.blit(surface, (10, 10 + index * 28))

    pygame.display.flip()


def reset_game():
    seeker = Agent('Seeker', 0, 0, SEEKER_COLOR)
    hider = Agent('Hider', SCREEN_WIDTH - 40, SCREEN_HEIGHT - 40, HIDER_COLOR)
    return seeker, hider, 0, False


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Hide and Seek AI')
    font = pygame.font.SysFont('Arial', 24)
    clock = pygame.time.Clock()

    seeker, hider, steps, caught = reset_game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                seeker, hider, steps, caught = reset_game()

        if not caught:
            dx, dy = hider_move(hider, seeker)
            hider.move(dx, dy)

            dx, dy = seeker_move(seeker, hider)
            seeker.move(dx, dy)

            steps += 1
            caught = seeker.distance_to(hider) == 0

        render(screen, font, seeker, hider, steps, caught)
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()

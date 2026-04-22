import pygame # Importuje knihovnu Pygame
import sys # Importuje systémový modul
import random # Importuje modul pro generování náhodných čísel+

pygame.init()

# Window Settings
Width = 1920
Height = 1080
Window = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Sphere") # Window title

# Colors variables
Black = (0, 0, 0)
White = (255, 255, 255)
Clock = pygame.time.Clock()

# Object Player
Sphere_radius = 25
Sphere_color = (0, 255, 0)
Sphere_x = Width // 2 - Sphere_radius // 2 
Sphere_y = Height // 2 - Sphere_radius // 2
Speed = 5
Death = False # Track if player is dead

# Object Coin
Coin_size = 20
Coin_color = (255, 215, 0)
Coin_x = Width // 2 - Coin_size // 2
Coin_y = Height // 3 - Coin_size // 2
Coin_collected = False # Track if coin has been collected



# Boss Settings
Boss_triangle_size = 160
Boss_triangle_color = (255 ,0 ,0) 
Boss_triangle_x = (Width // 2 - Boss_triangle_size // 2)
Boss_Speed = 6
GoLeft = False
# start above the window so the boss slides in
Boss_triangle_start_y = -Boss_triangle_size
Boss_triangle_y = Boss_triangle_start_y
Boss_triangle_target_y = (Height // 4 - Boss_triangle_size)
Boss_entry_speed = 3

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
Runs = True
while Runs: # Main game cycle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Runs = False # Ends the game loop

    # Input handling
    Keybind = pygame.key.get_pressed() # Shortcut 
    
    # Movement left and righht
    if Keybind[pygame.K_a] and Death == False: 
        Sphere_x -= Speed 
    if Keybind[pygame.K_d] and Death == False: 
        Sphere_x += Speed 

    # Movement up and down
    if Keybind[pygame.K_w] and Death == False:  
        Sphere_y -= Speed 
    if Keybind[pygame.K_s] and Death == False: 
        Sphere_y += Speed

    # Window boundaries
    Sphere_x = max(0, min(Sphere_x, Width - Sphere_radius * 2))
    Sphere_y = max(0, min(Sphere_y, Height - Sphere_radius * 2))
    # Collision detection between player and coin
    if not Coin_collected and (Sphere_x < Coin_x + Coin_size and
        Sphere_x + Sphere_radius * 2 > Coin_x and
        Sphere_y < Coin_y + Coin_size and       
        Sphere_y + Sphere_radius * 2 > Coin_y):
        # Collision detected
        Coin_collected = True # Makes the coin disappear

    # Collision detection between player and boss
    if Sphere_x < Boss_triangle_x + Boss_triangle_size and \
        Sphere_x + Sphere_radius * 2 > Boss_triangle_x and \
        Sphere_y < Boss_triangle_y + Boss_triangle_size and \
        Sphere_y + Sphere_radius * 2 > Boss_triangle_y:
        Death = True
        


    # Boss entrance animation
    if Coin_collected and Boss_triangle_y < Boss_triangle_target_y and not Death:
        Boss_triangle_y += Boss_entry_speed
        if Boss_triangle_y > Boss_triangle_target_y:
            Boss_triangle_y = Boss_triangle_target_y
    
    # Boss horizontal movement
    if Boss_triangle_y == Boss_triangle_target_y and not Death:
        Boss_triangle_x += Boss_Speed
        if Boss_triangle_x > Width - Boss_triangle_size and Boss_triangle_x != 0 and GoLeft == False:
            Boss_Speed = -8
            GoLeft = True
        elif Boss_triangle_x < 0 and Boss_triangle_x != 0 and GoLeft == True:
            Boss_Speed = +8
            GoLeft = False

    # Randomly Targets player with a 5% chance every frame // Phase 1        
    random_chance = random.randint(1, 50)
    if random_chance == 1 and Boss_triangle_y == Boss_triangle_target_y and not Death:
        if Sphere_x < Boss_triangle_x:
            Boss_Speed = -8
            GoLeft = True
        elif Sphere_x > Boss_triangle_x:
            Boss_Speed = +8
            GoLeft = False


    Window.fill(Black) # Resets window to full black
    # Rendering
    if not Coin_collected:
        pygame.draw.rect(Window, Coin_color, (Coin_x, Coin_y, Coin_size, Coin_size)) # Coin 

    pygame.draw.circle(Window, Sphere_color, (Sphere_x + Sphere_radius, Sphere_y + Sphere_radius), Sphere_radius) # Player

    # draw boss using current y (which animates when starting off-screen)
    pygame.draw.polygon(Window, Boss_triangle_color, [
        (Boss_triangle_x, Boss_triangle_y),
        (Boss_triangle_x + Boss_triangle_size, Boss_triangle_y),
        (Boss_triangle_x + Boss_triangle_size // 2, Boss_triangle_y + Boss_triangle_size)
    ]) # Boss triangle
        
    pygame.display.flip() # Updates the full display

    # Control FPS
    FPS = 60 # FPS value
    Clock.tick(FPS) # Caps FPS
pygame.quit()
sys.exit()
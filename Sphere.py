import pygame # Importuje knihovnu Pygame
import sys # Importuje systémový modul
import random # Importuje modul pro generování náhodných čísel+


# Inicialization of Pygame
pygame.init() # Inicializates Pygame

# Window Settings
Width = 1920
Height = 1080 
Window = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Sphere") # Window title

# Colors variables
Black = (0, 0, 0)
White = (255, 255, 255)

# Object Player
Sphere_radius = 25 # Nastaví velikost čtverce
Sphere_color = (255, 0, 0)
Sphere_x = Width // 2 - Sphere_radius // 2 # Vycentruje X souřadnici
Sphere_y = Height // 2 - Sphere_radius // 2 # Vycentruje Y souřadnici
rychlost = 5 # Nastaví rychlost pohybu

# Object Coin
Coin_size = 20
Coin_color = (255, 215, 0) # Gold color for the coin
Coin_x = Width // 2 - Coin_size // 2 # Default X pos
Coin_y = Height // 3 - Coin_size // 2 # Default Y pos
coin_collected = False # Track if coin has been collected



# Boss Settings
Boss_triangle_size = 40

# Enemy Settings
EnemyCount = 0
Enemies = [] # Enemies list
Size_Enemy = 30

# Nastavení písma pro zobrazení souřadnic
Font = pygame.font.SysFont("Arial", 24) # Nastaví písmo Arial velikost 24



# Hlavní smyčka
Runs = True # Nastaví pro smyčku
hodiny = pygame.time.Clock() # Vytvoří hodiny pro řízení FPS

while Runs: # Main game cycle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Runs = False # Ends the game loop

    # Input handling
    Keybind = pygame.key.get_pressed() # Shortcut 
    
    # Movement left and righht
    if Keybind[pygame.K_a]: 
        Sphere_x -= rychlost 
    if Keybind[pygame.K_d]: 
        Sphere_x += rychlost 

    # Movement up and down
    if Keybind[pygame.K_w]:  
        Sphere_y -= rychlost 
    if Keybind[pygame.K_s]: 
        Sphere_y += rychlost

    if Keybind[pygame.K_r]: #  reset position in the center
        Sphere_x = Width // 2 - Sphere_radius // 2 # Reset X position
        Sphere_y = Height // 2 - Sphere_radius // 2 # Reset Y position        

    # Window boundaries
    Sphere_x = max(0, min(Sphere_x, Width - Sphere_radius * 2)) # Zajišťuje, že čtverec nezmizí z okna horizontálně
    Sphere_y = max(0, min(Sphere_y, Height - Sphere_radius * 2)) # Zajišťuje, že čtverec nezmizí z okna vertikálně

    # Collision detection between player and coin
    if not coin_collected and (Sphere_x < Coin_x + Coin_size and
        Sphere_x + Sphere_radius * 2 > Coin_x and
        Sphere_y < Coin_y + Coin_size and       
        Sphere_y + Sphere_radius * 2 > Coin_y):
        # Collision detected
        EnemyCount += 1 # Increments enemy count by 1
        coin_collected = True # Makes the coin disappear
    # Vykreslení
    Window.fill(Black) # Resets window to full black
    

    # Rendering #
    if not coin_collected:
        pygame.draw.rect(Window, Coin_color, (Coin_x, Coin_y, Coin_size, Coin_size)) # Coin  
    pygame.draw.circle(Window, Sphere_color, (Sphere_x + Sphere_radius, Sphere_y + Sphere_radius), Sphere_radius) # Player
    
    # Zobrazení souřadnic
    text_souradnice = f"X: {Sphere_x}, Y: {Sphere_y}" 
    text_plocha = Font.render(text_souradnice, True, White) # Vytvoří obrázek textu
    Window.blit(text_plocha, (10, Height - 30)) # Vykreslí text do okna

    
    pygame.display.flip() # Updates the full display

    # Control FPS
    FPS = 60 # FPS value
    hodiny.tick(FPS) # Caps FPS

pygame.quit() # Ends pygame
sys.exit() # Ends the program
import pygame # Importuje knihovnu Pygame
import sys # Importuje systémový modul
import random # Importuje modul pro generování náhodných čísel+


# Inicialization of Pygame
pygame.init() # Inicializates Pygame

# Window Settings
Width = 1920
Height = 1080 
Window = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Cube") # Window title

# Colors variables
Black = (0, 0, 0)
White = (255, 255, 255)

# Object Settings(Cube) Player
Cube_size = 50 # Nastaví velikost čtverce
Cube_color = (255, 0, 0)
ctverec_x = Width // 2 - Cube_size // 2 # Vycentruje X souřadnici
ctverec_y = Height // 2 - Cube_size // 2 # Vycentruje Y souřadnici
rychlost = 5 # Nastaví rychlost pohybu

# Object Settings(Coin)
Size_Coin = 20
Coin_color = (255, 215, 0) # Gold color for the coin
Coin_x = Width // 2 - Size_Coin // 2 # Default X pos
Coin_y = Height // 3 - Size_Coin // 2 # Default Y pos

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
    for event in pygame.event.get(): # Načte všechny události
        if event.type == pygame.QUIT: # Pokud uživatel zavře okno
            Runs = False # Ukončí smyčku

    # Input handling
    Keybind = pygame.key.get_pressed() # Shortcut 
    
    # Pohyb zleva doprava
    if Keybind[pygame.K_a]: # Pokud je stisknuta šipka vlevo
        ctverec_x -= rychlost # Posune čtverec doleva
    if Keybind[pygame.K_d]: # Pokud je stisknuta šipka vpravo
        ctverec_x += rychlost # Posune čtverec doprava
        
    # Pohyb nahoru a dolu
    if Keybind[pygame.K_w]: # Pokud je stisknuta šipka nahoru
        ctverec_y -= rychlost # Posune čtverec nahoru
    if Keybind[pygame.K_s]: # Pokud je stisknuta šipka dolů
        ctverec_y += rychlost # Posune čtverec dolů

    if Keybind[pygame.K_r]: # Keybind R for reset position in the center
        ctverec_x = Width // 2 - Cube_size // 2 # Reset X position
        ctverec_y = Height // 2 - Cube_size // 2 # Reset Y position

    # Window boundaries
    ctverec_x = max(0, min(ctverec_x, Width - Cube_size)) # Zajišťuje, že čtverec nezmizí z okna horizontálně
    ctverec_y = max(0, min(ctverec_y, Height - Cube_size)) # Zajišťuje, že čtverec nezmizí z okna vertikálně

    # Collision detection between player and coin
    if (ctverec_x < Coin_x + Size_Coin and
        ctverec_x + Cube_size > Coin_x and
        ctverec_y < Coin_y + Size_Coin and
        ctverec_y + Cube_size > Coin_y):
        # Collision detected
        EnemyCount += 1 # Increments enemy count by 1

    # Vykreslení
    Window.fill(Black) # Resets window to full black
    

    # Rendering #
    pygame.draw.rect(Window, Coin_color, (Coin_x, Coin_y, Size_Coin, Size_Coin)) # Coin  
    pygame.draw.rect(Window, Cube_color, (ctverec_x, ctverec_y, Cube_size, Cube_size)) # Player
    
    # Zobrazení souřadnic
    text_souradnice = f"X: {ctverec_x}, Y: {ctverec_y}" 
    text_plocha = Font.render(text_souradnice, True, White) # Vytvoří obrázek textu
    Window.blit(text_plocha, (10, Height - 30)) # Vykreslí text do okna

    
    pygame.display.flip() # Updates the full display

    # Control FPS
    FPS = 60 # FPS value
    hodiny.tick(FPS) # Caps FPS

pygame.quit() # Ends pygame
sys.exit() # Ends the program
import pygame, sys
from menu_module import Menu, CounterInput
from game_module import Game
from layout_module import LayoutManager
from options_module import OptionsManager
from sound_module import SoundManager

#intiates pygame and clock
pygame.init()
clock = pygame.time.Clock()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w - 100, info.current_h - 100  # Slightly smaller than full screen

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Mormon Bridge")

layout = LayoutManager(screen)
options = OptionsManager(layout)
sounds = SoundManager()

# Colors
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

# Fonts
font = pygame.font.SysFont(None, 48)

# Screen state
current_screen = "menu"

# CounterInput (created once, used when needed)
playerCounter = CounterInput(layout, font, "Players", initial=4, min_val=2, max_val=6)

# Button action for Start Game
def start_game():
    global current_screen
    current_screen = "counter"

    pygame.event.clear()
    screen.blit(background, (0, 0))
    pygame.display.flip()
    pygame.time.wait(50)

    waiting_for_enter = True
    while waiting_for_enter:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            playerCounter.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN and playerCounter.enter_rect.collidepoint(event.pos):
                waiting_for_enter = False

        screen.blit(background, (0, 0))
        playerCounter.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    # Set up game instance and switch to game state
    global game_instance
    game_instance = Game(layout, sounds, options, screen, font, background, playerCounter.value)
    current_screen = "game"

#Button action for show Options
def show_options():
    global current_screen
    current_screen = "options"
    pygame.event.clear()
    options.run(screen)

#Button option for Quit Game
def quit_game():
    pygame.quit()
    sys.exit()

# Create menu
menu = Menu(layout, screen, font)
menu.add_button("Start", 0, 3, start_game)
menu.add_button("Options", 1, 3, show_options)
menu.add_button("Quit", 2, 3, quit_game)

# Main loop
running = True
result = None  # Track screen transitions

background = pygame.transform.scale(options.get_background(), (layout.width, layout.height))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_screen == "menu":
            menu.handle_event(event)
        elif current_screen == "counter":
            playerCounter.handle_event(event)

    if current_screen == "menu":
        menu.draw(background)

    elif current_screen == "game":
        result = game_instance.run()
        if result =="menu":
            background = options.get_background()
            current_screen = "menu"
            result = None
            
    elif current_screen == "options":
        result = options.run(screen)
        if result == "menu":
            background = options.get_background()
            current_screen = "menu"
        result = None

    elif current_screen == "counter":
        screen.blit(background, (0, 0))
        playerCounter.draw(screen)

    pygame.display.flip()

pygame.quit()

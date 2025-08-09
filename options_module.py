import pygame
from layout_module import LayoutManager

#controls GUI of options Screen
class OptionsManager:
    def __init__(self, layout: LayoutManager):
        self.layout = layout
        self.background_path = "background1.jpg"
        self.deck_path = "glider_deck"
        self.deck_options = ["glider_deck", "green_deck", "pheonix_deck", "pirates_deck", "spiderman_deck"]
        self.background_options = ["background1.jpg", "background2.jpg", "background3.png", "background4.png"]
        self.running = False

    #sets background image
    def set_background(self, background):
        self.background_path = background

    #sets deck folder
    def set_deck(self, deck):
        self.deck_path = deck

    #gets background image
    def get_background(self):
        return pygame.image.load(f"images/{self.background_path}").convert_alpha()

    # gets deck folder
    def get_deck(self):
        return self.deck_path

    #runs Options screen
    def run(self, screen):
        self.running = True
        font = self.layout.get_scaled_font(0.035)

        margin = 20
        spacing = 10
        button_width = self.layout.card_width
        button_height = self.layout.card_height

        while self.running:
            screen.fill((30, 30, 30))

            deck_buttons = []
            bg_buttons = []

            # Draw deck options
            for i, deck in enumerate(self.deck_options):
                x = margin + i * (button_width + spacing)
                y = margin
                rect = pygame.Rect(x, y, button_width, button_height)
                deck_buttons.append((rect, deck))

                if deck == self.deck_path:
                    pygame.draw.rect(screen, (255, 215, 0), rect.inflate(4, 4))  # Gold border

                pygame.draw.rect(screen, (70, 130, 180), rect)

                try:
                    deck_img = pygame.image.load(f"images/{deck}/back.jpg").convert_alpha()
                    deck_img = self.layout.scale_card(deck_img)
                    screen.blit(deck_img, (x, y))
                except Exception as e:
                    print(f"Missing deck image for {deck}: {e}")

            # Draw background options
            for i, bg in enumerate(self.background_options):
                x = margin + i * (button_width + spacing)
                y = margin + button_height + spacing
                rect = pygame.Rect(x, y, button_width, button_height)
                bg_buttons.append((rect, bg))

                if bg == self.background_path:
                    pygame.draw.rect(screen, (255, 215, 0), rect.inflate(4, 4))  # Gold border

                pygame.draw.rect(screen, (100, 180, 100), rect)

                try:
                    bg_img = pygame.image.load(f"images/backgrounds/{bg}").convert_alpha()
                    bg_img = self.layout.scale_card(bg_img)
                    screen.blit(bg_img, (x, y))
                except Exception as e:
                    print(f"Missing background image for {bg}: {e}")

            # Draw return button
            menu_y = screen.get_height() - button_height - margin
            return_rect = pygame.Rect(margin, menu_y, button_width, button_height)
            pygame.draw.rect(screen, (100, 100, 200), return_rect)
            screen.blit(font.render("Return to Home", True, (255, 255, 255)), (return_rect.x + 10, return_rect.y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos

                    for rect, deck in deck_buttons:
                        if rect.collidepoint(pos):
                            self.set_deck(deck)
                            print(f"Selected deck: {deck}")

                    for rect, bg in bg_buttons:
                        if rect.collidepoint(pos):
                            self.set_background(bg)
                            print(f"Selected background: {bg}")

                    if return_rect.collidepoint(pos):
                        self.running = False
                        return "menu"

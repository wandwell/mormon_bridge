import pygame, sys
from layout_module import LayoutManager

# Colors
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (30, 30, 30)

#Counter Class
class CounterInput:
    def __init__(self, layout: LayoutManager, font, label, initial=0, min_val=0, max_val=99):
        self.layout = layout
        self.font = font
        self.label = label
        self.value = initial
        self.min_val = min_val
        self.max_val = max_val

        label_width, label_height = 200, 50
        self.label_rect = self.layout.center_rect(label_width, label_height, y_offset=-40)
        self.minus_rect = pygame.Rect(self.label_rect.left - 50, self.label_rect.top, 40, label_height)
        self.plus_rect = pygame.Rect(self.label_rect.right + 10, self.label_rect.top, 40, label_height)

        enter_width, enter_height = 80, 30
        enter_x = self.label_rect.centerx - enter_width // 2
        enter_y = self.label_rect.bottom + 10
        self.enter_rect = pygame.Rect(enter_x, enter_y, enter_width, enter_height)

    #Draws counter on screen
    def draw(self, screen,):
        label_text = f"{self.label}: {self.value}"
        label_surf = self.font.render(label_text, True, WHITE)
        label_pos = label_surf.get_rect(center=self.label_rect.center)
        screen.blit(label_surf, label_pos)

        pygame.draw.rect(screen, GRAY, self.minus_rect)
        minus_surf = self.font.render("-", True, WHITE)
        screen.blit(minus_surf, minus_surf.get_rect(center=self.minus_rect.center))

        pygame.draw.rect(screen, GRAY, self.plus_rect)
        plus_surf = self.font.render("+", True, WHITE)
        screen.blit(plus_surf, plus_surf.get_rect(center=self.plus_rect.center))

        pygame.draw.rect(screen, GRAY, self.enter_rect)
        enter_surf = self.font.render("Enter", True, WHITE)
        screen.blit(enter_surf, enter_surf.get_rect(center=self.enter_rect.center))

    #handles what happens when buttons are clicked
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.minus_rect.collidepoint(event.pos):
                self.value = max(self.min_val, self.value - 1)
            elif self.plus_rect.collidepoint(event.pos):
                self.value = min(self.max_val, self.value + 1)

#MenuClass
class Menu:
    def __init__(self, layout: LayoutManager, screen, font):
        self.layout = layout
        self.screen = screen
        self.font = font
        self.buttons = []
        self.visible = True

    #adds button to menu
    def add_button(self, text, index, total, action):
        rect = self.layout.button_rect(index, total)
        self.buttons.append({"rect": rect, "text": text, "action": action})

    #draws menu on display
    def draw(self, background):
        if not self.visible:
            return

        self.screen.blit(background, (0, 0))
        for btn in self.buttons:
            pygame.draw.rect(self.screen, GRAY, btn["rect"])
            text_surf = self.font.render(btn["text"], True, WHITE)
            text_rect = text_surf.get_rect(center=btn["rect"].center)
            self.screen.blit(text_surf, text_rect)

        pygame.display.flip()

    #handle what happens when button is clicked
    def handle_event(self, event):
        if not self.visible:
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in self.buttons:
                if btn["rect"].collidepoint(event.pos):
                    btn["action"]()

                



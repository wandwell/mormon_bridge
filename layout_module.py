import pygame

# Class that controls the layout of the display
class LayoutManager:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

        # Core dimensions
        self.card_height = int(self.height * 0.2)
        self.card_width = int(self.card_height * 0.714)  # 5:7 aspect ratio
        self.spacing = int(self.width * 0.01)

        # Fonts
        self.font_size = int(self.height * 0.03)
        self.font = pygame.font.SysFont(None, self.font_size)

        # Buttons
        self.button_width = int(self.width * 0.15)
        self.button_height = int(self.height * 0.05)

    # Calculates horizontal positions for the current player's hand of cards
    def get_hand_position(self, num_cards: int) -> list[tuple[int, int]]:
        max_cards = 8
        cards_to_draw = min(num_cards, max_cards)
        total_width = cards_to_draw * (self.card_width + self.spacing) - self.spacing
        start_x = (self.width - total_width) // 2
        y = self.height - self.card_height - int(self.height * 0.02)

        return [(start_x + i * (self.card_width + self.spacing), y) for i in range(cards_to_draw)]

    # Returns screen positions for other players based on player count
    def get_player_positions(self, player_count: int) -> list[tuple[int, int]]:
        positions = [
            (self.width // 2, int(self.height * 0.05)),               # Top center
            (int(self.width * 0.05), self.height // 2),               # Left center
            (self.width - int(self.width * 0.10), self.height // 2), # Right center
            (self.width // 4, int(self.height * 0.10)),               # Top-left
            (3 * self.width // 4, int(self.height * 0.10)),           # Top-right
            (self.width // 2, self.height - self.card_height - int(self.height * 0.02)),  # Bottom center
        ]
        return positions[:player_count]

    # Determines position for a player's info box based on their location
    def get_info_box_position(self, player_index: int, player_count: int) -> tuple[int, int]:
        positions = self.get_player_positions(player_count)
        pos = positions[player_index]

        box_width, box_height = 110, 60
        x, y = pos

        if y < self.height // 3:  # Top
            y += 10
        elif y > 2 * self.height // 3:  # Bottom
            y -= box_height + 10
        else:  # Side
            y -= box_height // 2
            x += 120 if x < self.width // 2 else -box_width - 10

        return (x, y)

    # Scales a card image to the standard card dimensions
    def scale_card(self, image: pygame.Surface) -> pygame.Surface:
        return pygame.transform.scale(image, (self.card_width, self.card_height))

    # Returns a Rect for a button centered at the given position
    def get_button_rect(self, center: tuple[int, int]) -> pygame.Rect:
        x = center[0] - self.button_width // 2
        y = center[1] - self.button_height // 2
        return pygame.Rect(x, y, self.button_width, self.button_height)

    # Returns a Rect centered on screen with optional vertical offset
    def center_rect(self, width, height, y_offset=0) -> pygame.Rect:
        x = (self.width - width) // 2
        y = (self.height - height) // 2 + y_offset
        return pygame.Rect(x, y, width, height)

    # Calculates vertical button layout for a menu or dialog
    def button_rect(self, index, total, width=200, height=60, spacing=20) -> pygame.Rect:
        total_height = total * height + (total - 1) * spacing
        start_y = (self.height - total_height) // 2
        x = (self.width - width) // 2
        y = start_y + index * (height + spacing)
        return pygame.Rect(x, y, width, height)

    # Returns the center position for a single card
    def center_card_position(self) -> tuple[int, int]:
        x = self.width // 2 - self.card_width // 2
        y = self.height // 2 - self.card_height // 2
        return (x, y)

    # Returns the center position for text
    def center_text_position(self) -> tuple[int, int]:
        return (self.width // 2, self.height // 2)

    # Returns the position for displaying the trump card
    def trump_position(self) -> tuple[int, int]:
        return (self.width // 2 - self.card_width // 2, self.height // 2 + self.card_height // 2 + 10)

    # Returns a font scaled relative to screen height
    def get_scaled_font(self, size_ratio=0.03) -> pygame.font.Font:
        size = int(self.height * size_ratio)
        return pygame.font.SysFont(None, size)

    # Returns the file path for a suit icon image
    def get_suit_icon(self, suit):
        if suit == "Spades":
            return "images/icons/spade.png"
        elif suit == "Diamonds":
            return "images/icons/diamond.png"
        elif suit == "Hearts":
            return "images/icons/heart.png"
        elif suit == "Clubs":
            return "images/icons/club.png"
        else:
            return

    # Scales a suit icon image based on screen height
    def scale_icon(self, image: pygame.Surface, size_ratio: float = 0.1) -> pygame.Surface:
        size = int(self.height * size_ratio)
        return pygame.transform.scale(image, (size, size))

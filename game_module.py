import pygame, random
from player_module import Player
from deck_module import Deck, Card
from round_module import Round
from layout_module import LayoutManager
from menu_module import CounterInput
from options_module import OptionsManager
from sound_module import SoundManager

#Class containing GUI functions for game
class Game:
    def __init__(self, layout: LayoutManager, sounds: SoundManager, options: OptionsManager, screen, font, background, player_num):
        self.options = options
        self.screen = screen
        self.layout = layout
        self.sounds = sounds
        self.font = font
        self.small_font = pygame.font.Font(None, 16)
        self.background = background
        self.running = True
        self.player_num = player_num
        self.players: list[Player] = []
        self.deck = Deck(options)
        self.card_back_image = pygame.image.load("images/glider_deck/Back.jpg").convert_alpha()
        self.card_back_image = self.layout.scale_card(self.card_back_image)

    #animates the shuffle and plays sound
    def animate_shuffle(self):
        deck_center = self.layout.center_card_position()
        clock = pygame.time.Clock()
        num_cards = 20

        # Draw static center card once
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.card_back_image, deck_center)
        pygame.display.flip()
        self.sounds.play("shuffle")

        for i in range(num_cards):
            start_x = random.choice([0, self.screen.get_width()])
            start_y = random.randint(0, self.screen.get_height())

            for t in range(0, 11):
                x = start_x + (deck_center[0] - start_x) * t // 10
                y = start_y + (deck_center[1] - start_y) * t // 10

                # Redraw background but preserve center card
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.card_back_image, deck_center)
                self.screen.blit(self.card_back_image, (x, y))
                pygame.display.flip()
                clock.tick(60)

            # Stack effect
            offset_x = random.randint(-2, 2)
            offset_y = random.randint(-2, 2)
            self.screen.blit(self.card_back_image, (deck_center[0] + offset_x, deck_center[1] + offset_y))
            pygame.display.flip()
            pygame.time.delay(30)

        self.sounds.stop("shuffle")

    #animates dealing of cards and plays sound
    def animate_deal(self, round_instance):
        clock = pygame.time.Clock()
        deck_center = self.layout.center_card_position()

        # Draw static center card once
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.card_back_image, deck_center)
        pygame.display.flip()
        self.sounds.play("deal")

        for i in range(round_instance.num_of_cards):
            for player in self.players:
                target_pos = self.layout.get_player_positions(len(self.players))[player.id]
                target_x = target_pos[0] + i * 15
                target_y = target_pos[1]

                for t in range(0, 11):
                    x = deck_center[0] + (target_x - deck_center[0]) * t // 10
                    y = deck_center[1] + (target_y - deck_center[1]) * t // 10

                    self.screen.blit(self.background, (0, 0))
                    self.screen.blit(self.card_back_image, deck_center)
                    self.screen.blit(self.card_back_image, (x, y))
                    pygame.display.flip()
                    clock.tick(60)

                pygame.time.delay(50)
        self.sounds.stop("deal")

    #add players to game
    def addPlayers(self):
        for i in range(self.player_num):
            self.players.append(Player(self.screen, self.sounds, id=i))

    #draws the hand of the current player on display
    def draw_hand(self, player: Player, num_of_cards):
        positions = self.layout.get_hand_position(num_of_cards)

        # Assign positions
        for card, pos in zip(player.hand, positions):
            card.position = pos
            if card != player.dragging_card:
                card.rect.topleft = pos
                self.screen.blit(self.layout.scale_card(card.image), pos)

        # Draw dragging card last (if any)
        if player.dragging_card:
            self.screen.blit(
                self.layout.scale_card(player.dragging_card.image),
                player.dragging_card.rect.topleft
            )

    #draws the info box of the current Player
    def draw_player_info_box(self, player: Player):
        box_width, box_height = 90, 60
        box_x = 10
        box_y = self.screen.get_height() - box_height - 10

        # Create a semi-transparent surface
        info_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        info_surface.fill((0, 0, 0, 180))  # Black with alpha

        pygame.draw.rect(info_surface, (200, 200, 200), info_surface.get_rect(), 1)

        info_lines = [
            f"P{player.id + 1}",
            f"Bid:{player.bid} Trk:{player.tricks}",
            f"Scr:{player.score}"
        ]

        for i, line in enumerate(info_lines):
            text_surf = self.small_font.render(line, True, (255, 255, 255))
            info_surface.blit(text_surf, (5, 5 + i * 12))

        self.screen.blit(info_surface, (box_x, box_y))

    #draws the current cards in play
    def draw_trick_cards(self, played_cards: list[Card], winning_card: Card=None):
        card_width = self.card_back_image.get_width()
        spacing = 30
        total_width = len(played_cards) * card_width + (len(played_cards) - 1) * spacing
        start_x = (self.screen.get_width() - total_width) // 2
        y = self.screen.get_height() // 2 - card_width // 2

        for i, card in enumerate(played_cards):
            image = self.layout.scale_card(card.image)
            x = start_x + i * (card_width + spacing)
            self.screen.blit(image, (x, y))

            if card == winning_card:
                # Highlight with a glowing border
                pygame.draw.rect(
                    self.screen,
                    (255, 215, 0),  # Gold
                    pygame.Rect(x - 2, y - 2, image.get_width() + 4, image.get_height() + 4),
                    4
                )

    #draws both the icon of the trump suit and current suit with labels
    def draw_suit_icons(self, trump_suit: str, lead_suit: str = "none"):
        font = pygame.font.SysFont(None, 20)
        icon_y = self.layout.trump_position()[1]
        icon_x = self.layout.trump_position()[0]
        icon_spacing = 10
        label_to_icon_gap = 6  # 👈 Space between label and icon

        # Load trump icon
        trump_path = self.layout.get_suit_icon(trump_suit)
        trump_icon = None
        if trump_path:
            trump_icon = pygame.image.load(trump_path).convert_alpha()
            trump_icon = self.layout.scale_icon(trump_icon)

        # Load lead icon
        lead_path = self.layout.get_suit_icon(lead_suit) if lead_suit != "none" else None
        lead_icon = None
        if lead_path:
            lead_icon = pygame.image.load(lead_path).convert_alpha()
            lead_icon = self.layout.scale_icon(lead_icon)

        # Draw Trump label and icon
        if trump_icon:
            trump_label = font.render("Trump:", True, (255, 255, 255))
            label_rect = trump_label.get_rect(topleft=(icon_x, icon_y + trump_icon.get_height() // 2 - trump_label.get_height() // 2))
            self.screen.blit(trump_label, label_rect)

            trump_x = label_rect.right + label_to_icon_gap
            trump_rect = trump_icon.get_rect(topleft=(trump_x, icon_y))
            self._draw_glow(trump_rect)
            self.screen.blit(trump_icon, trump_rect)

            icon_x = trump_rect.right + icon_spacing

        # Draw Lead label and icon
        if lead_icon:
            lead_label = font.render("Suit:", True, (255, 255, 255))
            label_rect = lead_label.get_rect(topleft=(icon_x, icon_y + lead_icon.get_height() // 2 - lead_label.get_height() // 2))
            self.screen.blit(lead_label, label_rect)

            lead_x = label_rect.right + label_to_icon_gap
            lead_rect = lead_icon.get_rect(topleft=(lead_x, icon_y))
            self._draw_glow(lead_rect)
            self.screen.blit(lead_icon, lead_rect)

    # 🔆 Glow helper
    def _draw_glow(self, icon_rect):
        glow_radius = max(icon_rect.width, icon_rect.height) // 2 + 20
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        center = glow_radius

        for r in range(glow_radius, 0, -1):
            alpha = int(255 * ((glow_radius - r) / glow_radius) * 0.3)
            pygame.draw.circle(glow_surface, (255, 255, 255, alpha), (center, center), r)

        glow_rect = glow_surface.get_rect(center=icon_rect.center)
        self.screen.blit(glow_surface, glow_rect)

    # draws the back of the hands of other players along with info boxes
    def draw_other_players(self, current_player_id: int):
        opponents = [p for p in self.players if p.id != current_player_id]
        positions = self.layout.get_player_positions(len(self.players))
        opponent_positions = [pos for i, pos in enumerate(positions) if self.players[i].id != current_player_id]

        for player, pos in zip(opponents, opponent_positions):
            # Draw card backs
            if player.hand:
                for i in range(len(player.hand)):
                    offset_x = pos[0] + i * 15
                    self.screen.blit(self.card_back_image, (offset_x, pos[1]))
            else:
                # Draw faded placeholder
                faded = self.card_back_image.copy()
                faded.fill((100, 100, 100, 100), special_flags=pygame.BLEND_RGBA_MULT)
                self.screen.blit(faded, pos)

            # Get info box position from layout manager
            box_x, box_y = self.layout.get_info_box_position(player.id, len(self.players))

            # Draw info box
            pygame.draw.rect(self.screen, (30, 30, 30), (box_x, box_y, 60, 60))
            pygame.draw.rect(self.screen, (200, 200, 200), (box_x, box_y, 60, 60), 1)

            info_lines = [
                f"P{player.id + 1}",
                f"Bid: {player.bid}",
                f"Trk: {player.tricks}",
                f"Scr: {player.score}"
            ]

            for i, line in enumerate(info_lines):
                text_surf = self.small_font.render(line, True, (255, 255, 255))
                self.screen.blit(text_surf, (box_x + 5, box_y + 5 + i * 12))

    # displays the begin turn screen
    def show_begin_turn_screen(self, player_name):
        waiting = True
        button_rect = self.layout.center_rect(150, 40, y_offset=50)

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return "menu"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        waiting = False

            self.screen.blit(self.background, (0, 0))
            text = f"{player_name}, begin your turn!"
            text_surf = self.font.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.layout.center_text_position())
            self.screen.blit(text_surf, text_rect)

            pygame.draw.rect(self.screen, (0, 128, 0), button_rect)
            btn_text = self.font.render("Begin Turn", True, (255, 255, 255))
            btn_rect = btn_text.get_rect(center=button_rect.center)
            self.screen.blit(btn_text, btn_rect)

            pygame.display.flip()

    #runs the game
    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        self.addPlayers()
        played_cards: list[Card] = []

        for round_id in range(1, 16):
            if not self.running:
                break
            self.deck = Deck(self.options)
            self.animate_shuffle()
            round_instance = Round(id=round_id, deck=self.deck, players=self.players)
            round_instance.deal()
            self.animate_deal(round_instance)

            for player in self.players:
                bid_input = CounterInput(self.layout, self.font, f"Player {player.id + 1}: ", 0, 0, round_instance.num_of_cards)
                waiting_for_bid = True

                while waiting_for_bid and self.running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False
                            return "menu"
                        bid_input.handle_event(event)
                        if event.type == pygame.MOUSEBUTTONDOWN and bid_input.enter_rect.collidepoint(event.pos):
                            waiting_for_bid = False

                    self.screen.blit(self.background, (0, 0))

                    # Draw current player's hand
                    self.draw_hand(player, round_instance.num_of_cards)
                    self.draw_player_info_box(player)

                    # Draw trump suit (if known at this point)
                    self.draw_suit_icons(round_instance.trump)

                    # Draw bid input
                    bid_input.draw(self.screen)

                    pygame.display.flip()
                    clock.tick(60)

                player.bid = bid_input.value

            for turn_index in range(round_instance.num_of_cards):
                lead_suit = "none"
                for i in range(self.player_num):
                    player_index = (round_instance.leader_index + i) % self.player_num
                    current_player = round_instance.players[player_index]
                    self.show_begin_turn_screen(f"Player {current_player.id + 1}")

                    turn_active = True
                    played_card = None
                    while turn_active and self.running:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                self.running = False
                                return "menu"
                            played_card = current_player.play_card(lead_suit, pygame.mouse.get_pos(), event.type)
                            if played_card:
                                turn_active = False

                        self.screen.blit(self.background, (0, 0))
                        drop_zone = pygame.Rect(self.screen.get_width() // 2 - 50, self.screen.get_height() // 2 - 70, 100, 140)
                        pygame.draw.rect(self.screen, (200, 200, 200), drop_zone, 2)
                        self.draw_other_players(current_player.id)
                        self.draw_suit_icons(round_instance.trump, lead_suit)
                        self.draw_trick_cards(played_cards)
                        self.draw_hand(current_player, len(current_player.hand))
                        self.draw_player_info_box(current_player)
                        pygame.display.flip()
                        clock.tick(60)

                    current_card = round_instance.submit_card(current_player, played_card)
                    if player_index == round_instance.leader_index:
                        lead_suit = current_card.suit
                    played_cards.append(current_card)

                winning_card = round_instance.resolve_trick()
                self.screen.blit(self.background, (0, 0))
                self.draw_trick_cards(played_cards, winning_card)
                self.draw_suit_icons(round_instance.trump)
                pygame.display.flip()
                pygame.time.delay(1500)

                played_cards = []

            # Round summary
            round_instance.resolve_round()
            self.screen.blit(self.background, (0, 0))
            summary_text = f"Round {round_id} complete."
            summary_surf = self.font.render(summary_text, True, (255, 255, 255))
            summary_rect = summary_surf.get_rect(center=self.layout.center_text_position())
            self.screen.blit(summary_surf, summary_rect)
            pygame.display.flip()
            pygame.time.delay(1000)
        
        # Declare Winner
        winning_score = 0
        for player in self.players:
            if player.score > winning_score:
                winning_score = player.score
                winner = player

        # Game over screen
        self.screen.blit(self.background, (0, 0))
        game_over_surf = self.font.render(f"Game Over! Player {winner.id} Won!", True, (255, 255, 255))
        game_over_rect = game_over_surf.get_rect(center=self.layout.center_text_position())
        self.screen.blit(game_over_surf, game_over_rect)
        self.sounds.play("end")
        pygame.display.flip()
        pygame.time.delay(2000)
        self.sounds.stop("end")
        return "menu"

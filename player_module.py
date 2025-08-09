import pygame
from deck_module import Card
from sound_module import SoundManager

#Contains Player information and functions
class Player:
    def __init__(self, screen, sounds: SoundManager, id):
        self.screen = screen
        self.sounds = sounds
        self.dragging_card = None
        self.drag_offset = (0, 0)
        self.id = id
        self.hand = []
        self.turn = False
        self.tricks = 0
        self.score = 0
        self.bid = 0

    #adds hand to Player Object
    def add_hand(self, hand: list[Card]):
        for card in hand:
            self.hand.append(card)
            card.dealCard(self.id)

    # increases tricks won
    def add_trick(self):
        self.tricks = self.tricks + 1

    # sets bid for player
    def set_bid(self, bid):
        self.bid = bid

    #resets bid and tricks to 0
    def reset_bid(self):
        self.bid = 0
        self.tricks = 0

    #calculate players score based on tricks and bids
    def calculate_score(self):
        self.score = self.score + self.tricks
        if self.tricks == self.bid:
            self.score += 5

    # checks if Card matches suit
    def check_cards_for_suit(self, suit, played_card: Card):
        for card in self.hand:
            if card.id == played_card.id:
                continue
            if card.suit == suit:
                return True
        return False

    #checks if a player is allowed to play a certain Card
    def is_legal(self, suit, card: Card):
        return card.suit == suit or not self.check_cards_for_suit(suit, card)
  
    #Allows player to drag card to center to play card
    def play_card(self, suit, mouse_pos, event_type):
        if event_type == pygame.MOUSEBUTTONDOWN:
            for card in reversed(self.hand):  # Topmost first
                if card.rect.collidepoint(mouse_pos):
                    self.dragging_card = card
                    self.drag_offset = (mouse_pos[0] - card.rect.x, mouse_pos[1] - card.rect.y)
                    return None

        elif event_type == pygame.MOUSEMOTION and self.dragging_card:
            self.dragging_card.rect.topleft = (
                mouse_pos[0] - self.drag_offset[0],
                mouse_pos[1] - self.drag_offset[1]
            )

        elif event_type == pygame.MOUSEBUTTONUP and self.dragging_card:
            center_zone = pygame.Rect(
                self.screen.get_width() // 2 - 50,
                self.screen.get_height() // 2 - 70,
                100, 140
            )

            played = self.dragging_card

            if center_zone.collidepoint(mouse_pos):
                if self.is_legal(suit, played):
                    self.hand.remove(played)
                    self.dragging_card = None
                    self.sounds.play("correct")
                    return played
                else:
                    # Dropped in center but illegal
                    played.rect.topleft = played.position
                    self.dragging_card = None
                    self.sounds.play("wrong")
            else:
                # Dropped outside center — no sound
                played.rect.topleft = played.position
                self.dragging_card = None

        return None

    
        


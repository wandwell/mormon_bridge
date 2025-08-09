import pygame
import json, random
from options_module import OptionsManager

#Class to Store individual Card information
class Card:
    #Class init function
    def __init__(self, id, rank, suit, value, image):
        self.id = id
        self.rank = rank
        self.suit = suit
        self.value = value
        self.image = image
        self.player_id = None
        self.position = (0, 0)  
        self.rect = pygame.Rect(0, 0, 100, 140)  

    # decides if Card is in the trump suit or not
    def is_trump(self, trump):
        if self.suit == trump:
            return True
        else:
            return False

    #   decides if Card belongs to particular Suit 
    def is_correct_suit(self, suit):
        if self.suit == suit:
            return True
        else:
            return False

    # places image of Card on display   
    def draw(self, surface, position):
        if self.image:
            self.position = position
            self.rect.topleft = position
            surface.blit(self.image, position)

    #assigns player_id to Card
    def dealCard(self, player_id):
        self.player_id = player_id

#Class to hold Cards in the Deck
class Deck:
    def __init__(self, options: OptionsManager):
        self.deck_path = options.get_deck()
        self.cards = []
        self.load_deck("deck.json")
        self.shuffleDeck()

    #Creates Cards according to information in deck.json
    def load_deck(self, json_path):
        try:
            with open(json_path, 'r') as file:
                data = json.load(file)
                for card_data in data.get("cards", []):
                    image_path = f"images/{self.deck_path}/{card_data["id"]}.jpg"
                    image = pygame.image.load(image_path).convert_alpha() if image_path else None

                    card = Card(
                        id=card_data["id"],
                        rank=card_data["rank"],
                        suit=card_data["suit"],
                        value=card_data["value"],
                        image=image
                    )
                    self.cards.append(card)
        except FileNotFoundError:
            print(f"Error: {json_path} not found.")
        except json.JSONDecodeError:
            print(f"Error: Failed to parse {json_path}.")
        except pygame.error as e:
            print(f"Image loading error: {e}")

    #shuffles Deck
    def shuffleDeck(self):
        random.shuffle(self.cards)

    #returns list of cards
    def deal_cards(self, count: int) -> list[Card]:
        if count > len(self.cards):
            raise ValueError("Not enough cards left in the deck to deal.")
        dealt = self.cards[:count]
        self.cards = self.cards[count:]
        return dealt

    # returns list of hands
    def deal_to_players(self, num_players, cards_per_player):
        if num_players * cards_per_player > len(self.cards):
            raise ValueError("Not enough cards to deal to all players.")
        hands = []
        for _ in range(num_players):
            hands.append(self.deal_cards(cards_per_player))
        return hands
    
    # decides trump by dealing Card
    def choose_trump(self) -> str:
        if not self.cards:
            raise ValueError("No cards left in the deck to choose a trump.")
        trump_card = self.deal_cards(1)[0]
        return trump_card.suit
    
    #updates position in display
    def update_position(self, pos):
        self.position = pos
        self.rect.topleft = pos



    



    

import pygame
from deck_module import Deck, Card
from player_module import Player

#controls information for the Round
class Round:
    def __init__(self, id: int, deck: Deck, players: list[Player]):
        self.id = id
        self.players = players
        self.num_of_players = len(players)
        self.deck = deck
        self.leader_index = 0
        self.played_cards = []
        self.num_of_cards = id if id <= 8 else 16 - id
        self.hands = deck.deal_to_players(self.num_of_players, self.num_of_cards)
        self.trump = deck.choose_trump()

    #Passes hands to players
    def deal(self):
        for i in range(self.num_of_players):
            self.players[i].add_hand(self.hands[i])

    # enters a Card into play
    def submit_card(self, player: Player, card: Card):
        self.played_cards.append((player, card))
        return card

    #resolves each "trick" or turn
    def resolve_trick(self):
        lead_player, lead_card = self.played_cards[0]
        lead_suit = lead_card.suit
        winning_card = lead_card
        winning_player = lead_player

        for player, card in self.played_cards[1:]:
            if card.is_trump(self.trump):
                if not winning_card.is_trump(self.trump) or card.value > winning_card.value:
                    winning_card = card
                    winning_player = player
            elif card.is_correct_suit(lead_suit) and not winning_card.is_trump(self.trump):
                if card.value > winning_card.value:
                    winning_card = card
                    winning_player = player

        winning_player.add_trick()
        self.leader_index = self.players.index(winning_player)
        return winning_card

    #resolves the round
    def resolve_round(self):
        for player in self.players:
            player.calculate_score()
            player.reset_bid()

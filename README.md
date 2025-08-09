# Overview

A basic Mormon Bridge Game to learn how to use pygame and better understand game frameworks

Mormon Bridge can be played by 2 - 6 players, although most common is 4.

There are 15 rounds. In rounds 1 - 8 the number of cards increases by 1 and in rounds 9 - 15 it decreases by 1. So each player recieves by round

- 1: 1 Card
- 2: 2 Cards
- 3: 3 Cards
- 4: 4 Cards
- 5: 5 Cards
- 6: 6 Cards
- 7: 7 Cards
- 8: 8 Cards
- 9: 7 Cards
- 10: 6 Cards
- 11: 5 Cards
- 12: 4 Cards
- 13: 3 Cards
- 14: 2 Cards
- 15: 1 Card

After the correct number of cards is dealt to the players, a trump card is dealt. The suit of the trump card is trump for that round. Each round is separated into tricks. At the beginning of each round, every player 'bids' or states how many tricks they think they can win. That bid is recorded and the player is trying to match their bid, neither going over or under.

A trick is begins when player 1 lays down their card. The rest of the players have to match the suit of the first card if possible, only using other cards if their is not a card of that suit in their hand. The following players need to get a higher card than the others played to win. For example, if Player 2 and Player 3 both play a 10 and this is the highest card, Player 2 wins the trick.

At the end of the round a player gets 1 point for each trick they won. If they matched their bid, they get a 5 additional points. At the end of the game, the person with the highest score wins

[Software Demo Video](https://youtu.be/CoWFgJnuGsA)

# Development Environment

- Pygame

Libraries

- Random
- pygame.mixer

# Useful Websites

- [pygame docs](https://www.pygame.org/docs/)
- [Pixabay](https://pixabay.com/sound-effects/)
- [aspiesmagic](https://www.flickr.com/photos/167981955@N07/albums/)

# Future Work

- Make it so people can play from different devices
- Continue to fine tune and improve transitions
- Put a hamburger menu in game screen so players can return to menu

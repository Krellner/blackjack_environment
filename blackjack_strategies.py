"""Blackjack strategies module.

MIT License

Copyright (c) 2025 Florian Krellner

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import Any

def calculate_hand_value(hand: list) -> int:
        """Calculate the value of a hand in blackjack.

        Args:
            hand (list): List of cards in the hand.
        Returns:
            int: Total value of the hand.
        """        
        value = 0
        aces = 0

        for card in hand:
            if card in ['J', 'Q', 'K']:
                value += 10
            elif card == 'A':
                aces += 1
                value += 11  # Initially count Ace as 11
            else:
                value += int(card)
        # Adjust for Aces if value exceeds 21
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

def basic(player_hand: list, dealer_upcard: str) -> bool:
    """A simple player strategy: hit if hand value < 17, else stand.
    
    Args:
        player_hand (list): Player's hand.
        dealer_upcard (str): Dealer's visible card.
    Returns:
        bool: True to hit, False to stand.
    """
    return calculate_hand_value(player_hand) < 17


class PlayerStrategy:
    """Class to encapsulate player strategy functions."""

    def __init__(self, n_card_decks=1) -> None:
        """Initialize the PlayerStrategy with either a basic or trained strategy.

        Args:
            n_card_decks (int): Number of decks to use in training the strategy.
        """ 
        self.n_card_decks = n_card_decks
        self.strategy = self.train_strategy(n_card_decks)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.strategy(*args, **kwds)

    def train_strategy(self, n_card_decks: int) -> callable:
        """Train a player strategy using reinforcement learning.
        
        Args:
            n_card_decks (int): Number of decks to use in training.
        """
        # TODO: add training logic here

        # TODO: for now, return basic strategy
        return basic
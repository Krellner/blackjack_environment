"""Blackjack environment core module.

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

import random, argparse
from blackjack_strategies import PlayerStrategy

CARD_DECK = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4  # Standard 52-card deck

class BlackjackGame:

    def __init__(self, n_card_decks: int, logging=True) -> None:
        """Initialize a game of blackjack with n_card_decks decks of cards.

        Args:
            n_card_decks (int): Number of decks to use in the game.
            logging (bool, optional): Whether to log game events. Defaults to True.
        """
        self.n_card_decks = n_card_decks
        self.logging = logging

        # Create and shuffle the combined decks
        self.cards = CARD_DECK * self.n_card_decks
        random.shuffle(self.cards)

    def deal_card(self) -> str:
        """Deal a single card from the deck.

        Returns:
            str: The dealt card.
        """
        return self.cards.pop()
    
    def calculate_hand_value(self, hand: list) -> int:
        """Calculate the value of a hand in blackjack.

        Args:
            hand (list): List of cards in the hand.
        Returns:
            int: The total value of the hand.
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
    
    def determine_winner(self, player_hand: list, dealer_hand: list) -> str:
        """Determine the winner of the game.

        Args:
            player_hand (list): Player's hand.
            dealer_hand (list): Dealer's hand.
        Returns:
            str: Result of the game ('win', 'lose', 'draw').
        """        
        player_value = self.calculate_hand_value(player_hand)
        dealer_value = self.calculate_hand_value(dealer_hand)

        if player_value > 21:
            return 'lose'
        elif dealer_value > 21 or player_value > dealer_value:
            return 'win'
        elif player_value < dealer_value:
            return 'lose'
        else:
            return 'draw'
    
    def play(self, player_strategy) -> str:
        """Play a round of blackjack between a player and a dealer.

        Args:
            player_strategy (callable): Function that determines player's actions.
        Returns:
            str: Result of the game ('win', 'lose', 'draw').
        """ 
        player_hand = [self.deal_card(), self.deal_card()]
        dealer_hand = [self.deal_card(), self.deal_card()]

        if self.logging:
            print(f"Player's hand: {player_hand}")
            print(f"Dealer's hand: {dealer_hand[0]}, ?")

        # Player's turn
        while player_strategy(player_hand, dealer_hand[0]):
            player_hand.append(self.deal_card())
            if self.logging:
                print(f"Player hits: {player_hand}")

        # Dealer's turn
        while self.calculate_hand_value(dealer_hand) < 17:
            dealer_hand.append(self.deal_card())
            if self.logging:
                print(f"Dealer hits: {dealer_hand}")

        if self.logging:
            print(f"Final Player's hand: {player_hand} (value: {self.calculate_hand_value(player_hand)})")
            print(f"Final Dealer's hand: {dealer_hand} (value: {self.calculate_hand_value(dealer_hand)})")

        return self.determine_winner(player_hand, dealer_hand)
        
    def reset(self) -> None:
        """Reset the game by reshuffling the decks."""
        self.cards = CARD_DECK * self.n_card_decks
        random.shuffle(self.cards)

    def experiment(self, n_runs: int, player_strategy: callable) -> dict:
        """Run multiple games of blackjack and collect statistics.

        Args:
            n_runs (int): Number of games to run.
            player_strategy (callable): Function that determines player's actions.   
        Returns:
            dict: Statistics of wins, losses, and draws.
        """
        results = {'win': 0, 'lose': 0, 'draw': 0}

        for _ in range(n_runs):
            result = self.play(player_strategy)
            results[result] += 1
            self.reset()

        return results
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play a game of Blackjack or run multiple simulations.")
    parser.add_argument("--decks", type=int, default=1, help="Number of card decks to use (default: 1)")
    parser.add_argument("--runs", type=int, default=0, help="Number of games to simulate (0 = play a single logged game)")
    parser.add_argument("--no-log", action="store_true", help="Disable logging output for a single game run")
    args = parser.parse_args()

    n_card_decks = args.decks

    game = BlackjackGame(n_card_decks=n_card_decks, logging=not args.no_log)
    strategy = PlayerStrategy(n_card_decks)

    if args.runs > 1:
        stats = game.experiment(args.runs, strategy)
        total = sum(stats.values())
        win_rate = stats['win'] / total if total else 0.0
        lose_rate = stats['lose'] / total if total else 0.0
        draw_rate = stats['draw'] / total if total else 0.0
        print(f"Ran {total} games with {n_card_decks} deck(s).")
        print(f"Wins: {stats['win']} ({win_rate:.2%}) | Losses: {stats['lose']} ({lose_rate:.2%}) | Draws: {stats['draw']} ({draw_rate:.2%})")
    else:
        result = game.play(strategy)
        print(f"Game result: {result}")
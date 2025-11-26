# Blackjack Environment

A minimal, extensible Blackjack simulation environment with a pluggable player strategy interface. Useful for quick probability experiments, reinforcement learning prototypes, or basic game simulations.

## Features
- Simple `BlackjackGame` engine with multi-deck support.
- Pluggable player strategy via `PlayerStrategy` callable wrapper.
- Built-in basic strategy (hit < 17) as default placeholder.
- Simulation mode for bulk runs (`experiment`).
- MIT licensed.

## Requirements
- Python >= 3.9

## Installation
Clone the repository and install locally:
```bash
git clone https://github.com/Krellner/blackjack_environment.git
cd blackjack_environment
pip install .
```
Editable (development) install:
```bash
pip install -e .
```
Build a wheel/distribution (optional):
```bash
python -m pip install --upgrade build
python -m build
```
Then install the generated wheel in `dist/` if desired:
```bash
pip install dist/blackjack_environment-0.1.0-py3-none-any.whl
```

## Module Import Usage
After installation you can import the modules directly:
```python
from blackjack import BlackjackGame
from blackjack_strategies import PlayerStrategy, basic

# Single game
game = BlackjackGame(n_card_decks=1, logging=True)
strategy = PlayerStrategy(1)  # wraps the current trained/basic strategy
result = game.play(strategy)
print("Result:", result)

# Bulk simulation
game = BlackjackGame(n_card_decks=4, logging=False)
strategy = PlayerStrategy(4)
stats = game.experiment(n_runs=10_000, player_strategy=strategy)
print(stats)
```

## Command-Line Usage
You can run the engine script directly (the `if __name__ == "__main__"` block in `blackjack.py` handles arguments):
```bash
python blackjack.py --decks 4 --runs 1000
```
Or, once installed, invoke as a module:
```bash
python -m blackjack --decks 2 --runs 5000
```
Arguments:
- `--decks <int>`: Number of card decks (default 1)
- `--runs <int>`: Number of simulations (>1 triggers batch mode) (default 0)
- `--no-log`: Suppress per-action logging for a single game

Single logged game example:
```bash
python blackjack.py --decks 1
```

## Strategy Customization
The `PlayerStrategy` class currently returns the `basic` strategy. You can supply your own directly to `play` or `experiment`:
```python
def conservative(player_hand, dealer_upcard):
    # Stand on 16+ and never hit on soft 18+
    from blackjack_strategies import calculate_hand_value
    value = calculate_hand_value(player_hand)
    return value < 16

from blackjack import BlackjackGame

custom_game = BlackjackGame(2, logging=False)
result = custom_game.play(conservative)
print("Custom result:", result)
```
To integrate a trained RL policy, modify `train_strategy` in `blackjack_strategies.py` to return a function with signature `(player_hand: list, dealer_upcard: str) -> bool`.

## API Overview
- `BlackjackGame(n_card_decks: int, logging: bool)`
  - `play(player_strategy: callable) -> str` returns `'win' | 'lose' | 'draw'`.
  - `experiment(n_runs: int, player_strategy: callable) -> dict` returns counts `{'win': int, 'lose': int, 'draw': int}`.
  - `reset()` reshuffles the combined decks.
- `PlayerStrategy(n_card_decks: int)` callable returning underlying strategy.
- Helper: `calculate_hand_value(hand: list) -> int` (duplicated logic also inside `BlackjackGame`).

## Notes & Extensibility
- For improved realism (splits, doubling down, insurance) extend `BlackjackGame` with additional state and decision layers.
- For performance in large simulations, consider replacing Python lists with `deque` or vectorized approaches; current design favors readability.
- Deterministic testing: inject a seeded shuffle (e.g. replace `random.shuffle` with a deterministic wrapper when `logging` is False).

## License
MIT License. See `LICENSE` for the full text.

## Contributing
1. Fork & branch.
2. Add/adjust strategies or engine features.
3. Submit PR with concise description & benchmarks if adding heavy simulation features.


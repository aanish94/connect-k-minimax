# Connect-K Minimax Implementation

This repository applies the Minimax algorithm to the game of Connect-k. Connect-k is played on a vertically suspended grid with m columns and n rows,
or (m, n, k)-game for short. The classic game of Connect-4 can be taken to be the (m=7, n=6, k=4) game.

The Minimax algorithm is an adverserial search algorithm which enables agents to make strategic decisions. Minimax is a recursive algorithm that generates and traverses a game tree which collects all possibles states and actions of the game. The algorithm has a MAX player which aims to maximize value and a MIN player which aims to minimize the value of the MAX player.

## Results

#### MiniMax w/ depth=4 (easy)

![Game Run](https://github.com/aanish94/connect-k-minimax/blob/main/results/depth4.gif)

#### MiniMax w/ depth=5 (medium)

![Game Run 2](https://github.com/aanish94/connect-k-minimax/blob/main/results/depth5.gif)

## Instructions

The following simulations all run the Connect-4 game with different player options.

```bash
python simulation.py 0  # Minimax vs Random
python simulation.py 1  # Human vs Minimax
python simulation.py 2  # Max vs Min
python simulation.py 3  # Human assisted Max vs Min
python simulation.py 4 100 # Random vs Random, plays 100 games
python simulation.py 5  # Human vs Human
python simulation.py 6  # Human vs Random
```

## Project Structure

#### `main.py`

This is the primary script that implements the Game and Board class.

#### `player.py`

This implements the Player class which includes HumanPlayer, RandomPlayer and a MiniMax Player.

#### `simulation.py`

This script allows to run multiple simulations such as MiniMax vs. Human.

#### `evaluate.py`

This script evaluates the performance of the MiniMax algorithm with and without pruning.

import argparse

from main import Game
from player import Human, RandomComputer, MiniMax

PLAYER1_PIECE = 1
PLAYER2_PIECE = 2


def report_results(results, player1, player2):
    """
    Reports the results of the games
    """

    print(f"Player 1 wins: {results.count(player1.piece)}")
    print(f"Player 2 wins: {results.count(player2.piece)}")
    print(f"Draws: {results.count(0)}")


def HumanVsHumanConnect4(num_games=1):
    player1 = Human(PLAYER1_PIECE)
    player2 = Human(PLAYER2_PIECE)

    game = Game(player1, player2, 7, 6, 4)
    game.play()


def HumanVsRandomConnect4(num_games=1):
    player1 = Human(PLAYER1_PIECE)
    player2 = RandomComputer(PLAYER2_PIECE)

    game = Game(player1, player2, 7, 6, 4)
    game.play()


def RandomVsRandomConnect4(num_games=1):
    player1 = RandomComputer(PLAYER1_PIECE)
    player2 = RandomComputer(PLAYER2_PIECE)

    results = []
    for _ in range(num_games):
        game = Game(player1, player2, 7, 6, 4)
        winner, _, _ = game.play(quiet=True)
        results.append(winner)

    report_results(results, player1, player2)


def MiniMaxVsRandomConnect4(num_games=1):
    player1 = MiniMax(
        PLAYER1_PIECE,
        PLAYER2_PIECE,
        max_player=True,
        use_heuristic=True,
    )
    player2 = RandomComputer(PLAYER2_PIECE)

    game = Game(player1, player2, 7, 6, 4)
    game.play()


def MiniMaxVsHumanConnect4(num_games=1):
    player1 = Human(PLAYER1_PIECE)
    player2 = MiniMax(
        PLAYER2_PIECE,
        PLAYER1_PIECE,
        max_player=False,
        use_heuristic=True,
    )

    game = Game(player1, player2, 7, 6, 4)
    game.play()


def MiniMaxVsMiniMax(num_games=1):
    player1 = MiniMax(
        piece=PLAYER1_PIECE,
        opponent_piece=PLAYER2_PIECE,
        max_player=True,
        depth=4,
        use_heuristic=True,
    )

    player2 = MiniMax(
        piece=PLAYER2_PIECE,
        opponent_piece=PLAYER1_PIECE,
        max_player=False,
        depth=4,
        use_heuristic=True,
    )

    game = Game(player1, player2, 7, 6, 4)
    game.play()


def HumanMiniMaxVsMiniMax(num_games=1):
    player1 = MiniMax(
        piece=PLAYER1_PIECE,
        opponent_piece=PLAYER2_PIECE,
        max_player=True,
        depth=4,
        autopilot=False,
        use_heuristic=True,
    )

    player2 = MiniMax(
        piece=PLAYER2_PIECE,
        opponent_piece=PLAYER1_PIECE,
        max_player=False,
        depth=4,
        use_heuristic=True,
    )

    game = Game(player1, player2, 7, 6, 4)
    game.play()


def main():

    simulations = [
        MiniMaxVsRandomConnect4,
        MiniMaxVsHumanConnect4,
        MiniMaxVsMiniMax,
        HumanMiniMaxVsMiniMax,
        RandomVsRandomConnect4,
        HumanVsHumanConnect4,
        HumanVsRandomConnect4,
    ]

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run a Connect-k game or simulation.")

    # Add optional arguments
    parser.add_argument(
        "sim",
        type=int,
        nargs="?",
        default=0,
        help="Index of the game (default: 0)"
    )

    parser.add_argument(
        "num_games",
        type=int,
        nargs="?",
        default=1,
        help="Number of games to play (default: 1)"
    )

    # Parse arguments
    args = parser.parse_args()

    # Use the arguments
    idx = args.sim
    num_games = args.num_games

    # Run the simulation
    simulation = simulations[idx]
    simulation(num_games)


if __name__ == "__main__":
    main()

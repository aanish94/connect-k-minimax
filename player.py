import math
import numpy as np
import random


class Player:
    """
    Player class
    """

    def __init__(self, piece):
        self.piece = piece


class Human(Player):
    """
    Human class
    """

    def select_move(self, board):
        """
        Selects a move
        """

        col = int(input(f"Player {self.piece} - choose a column to play: ")) - 1
        while not board.is_valid(col):
            print("Invalid input, try again")
            col = int(input("Choose a column to play: ")) - 1
        return col


class RandomComputer(Player):
    """
    RandomComputer class
    """

    def select_move(self, board):
        """
        Selects a move
        """

        return random.choice(board.get_valid_locations())


class MiniMax(Player):

    def __init__(
            self,
            piece,
            opponent_piece,
            max_player,
            alpha_beta_pruning=True,
            depth=4,
            use_heuristic=False,
            autopilot=True,
    ):
        """
        Initializes the MiniMax player
        :param piece: int, represents the player's piece
        :param opponent_piece: int, represents the opponent's piece
        :param max_player: bool, True if player is maximizer, False if player is minimizer
        :param alpha: int, pruning parameter
        :param beta: int, pruning parameter
        :param depth: int, depth of the search tree
        :param use_heuristic: bool, True if heuristic evaluation function is used
        :param autopilot: bool, True if AI selects moves automatically
        """

        super().__init__(piece)
        self.opponent_piece = opponent_piece
        self.max_player = max_player
        if alpha_beta_pruning:
            self.alpha = -math.inf
            self.beta = math.inf
        else:
            self.alpha = None
            self.beta = None
        self.depth = depth
        self.use_heuristic = use_heuristic
        self.counter = 0
        self.autopilot = autopilot

    def select_move(self, board):
        """
        Selects a move
        """

        self.counter = 0
        _, action = self.minimax(
            board, self.depth, self.alpha, self.beta, self.max_player, self.use_heuristic,
        )

        if self.autopilot:
            return action
        else:
            print(f"MiniMax recommended action: {action+1}")
            col = int(input(f"Player {self.piece} - choose a column to play: ")) - 1
            return col

    def minimax(
            self,
            board,
            depth,
            alpha,
            beta,
            max_player,
            use_heuristic=False,
    ):
        """
        Minimax algorithm with alpha-beta pruning

        :param board: Board, current board state
        :param depth: int, depth of the search tree
        :param alpha: int, pruning parameter
        :param beta: int, pruning parameter
        :param max_player: bool, True if player is maximizer, False if player is minimizer
        :param use_heuristic: bool, True if heuristic evaluation function is used

        :return: int, column of the best move
        :return: int, value of the best move
        """

        self.counter += 1

        # Check if a terminal state has been reached
        is_terminal, winner = board.is_terminal()
        if is_terminal:
            # Return positive value if player wins, negative value if opponent wins
            if winner == self.piece:
                return (math.inf, None)
            elif winner == self.opponent_piece:
                return (-math.inf, None)
            else:
                return (0, None)  # Draw utility value

        # Check if depth limit has been reached
        if depth == 0 and use_heuristic:
            score = self.heuristic(board, self.piece, self.opponent_piece)
            return (score, None)

        # Get all possible actions
        locations = board.get_valid_locations()

        # Max Player
        if max_player:
            # Default values
            value = -math.inf
            column = None

            # Iterate over all possible columns where the player can place a piece
            # and simulate by adding a piece to the board and evaluating the state
            for action in locations:
                row, col = board.add_piece(action, self.piece)
                new_score, _ = self.minimax(
                    board, depth - 1, alpha, beta, False, use_heuristic,
                )

                # Update the value and column if a max move is found
                if new_score > value:
                    value = new_score
                    column = action

                # Undo the move to prevent altering the board permanently
                board.remove_piece(row, col)

                # Alpha-beta pruning
                if alpha:
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break

            return value, column
        # Min Player
        else:
            value = math.inf
            column = None

            # Iterate over all possible columns where the opponent can place a piece
            # and simulate by adding a piece to the board and evaluating the state
            for action in locations:
                row, col = board.add_piece(action, self.opponent_piece)
                new_score, _ = self.minimax(
                    board, depth - 1, alpha, beta, True, use_heuristic,
                )

                # Update the value and column if a min move is found
                if new_score < value:
                    value = new_score
                    column = action

                # Undo the move to prevent altering the board permanently
                board.remove_piece(row, col)

                # Alpha-beta pruning
                if beta:
                    beta = min(beta, value)
                    if alpha >= beta:
                        break

            return value, column

    def heuristic(self, board, piece, opponent_piece):
        """
        Heuristic evaluation function for the MiniMax algorithm
        """

        return score_position(board, piece, opponent_piece)


def score_position(board, piece, opponent_piece):
    """
    Computes the heuristic score for the given board state.
    """
    ROWS, COLS = board.ROWS, board.COLS
    score = 0

    # Favor center column to promote central control
    center_column = board[:, COLS // 2]
    center_count = np.sum(center_column == piece)
    score += center_count * 3

    # Check horizontal windows
    for row in range(ROWS):
        for col in range(COLS - 3):  # 4 consecutive cells
            window = board[row, col:col + 4]
            score += evaluate_window(window, piece, opponent_piece)

    # Check vertical windows
    for row in range(ROWS - 3):
        for col in range(COLS):
            window = board[row:row + 4, col]
            score += evaluate_window(window, piece, opponent_piece)

    # Check positive diagonal windows
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [board[row + i, col + i] for i in range(4)]
            score += evaluate_window(window, piece, opponent_piece)

    # Check negative diagonal windows
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = [board[row - i, col + i] for i in range(4)]
            score += evaluate_window(window, piece, opponent_piece)

    return score


def evaluate_window(window, piece, opponent_piece):
    """
    Evaluates a 4-cell window to assign a score based on its composition.
    """
    score = 0
    player_count = np.sum(window == piece)
    opponent_count = np.sum(window == opponent_piece)
    empty_count = np.sum(window == 0)

    # Favorable configurations for the player
    if player_count == 4:
        score += math.inf  # Winning condition
    elif player_count == 3 and empty_count == 1:
        score += 10  # Strong potential
    elif player_count == 2 and empty_count == 2:
        score += 5   # Weak potential

    # Penalize opponent's configurations
    if opponent_count == 4:
        score -= math.inf  # Opponent's winning condition
    elif opponent_count == 3 and empty_count == 1:
        score -= 10  # Opponent's strong potential
    elif opponent_count == 2 and empty_count == 2:
        score -= 5   # Opponent's weak potential

    return score

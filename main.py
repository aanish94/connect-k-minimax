import matplotlib.pyplot as plt
import numpy as np
import time

from player import Human, RandomComputer, MiniMax


class Board:

    def __init__(self, cols, rows, k):
        """
        Class represents the game board
        """

        self.COLS = cols
        self.ROWS = rows
        self.k = k

        self.board = np.zeros((self.ROWS, self.COLS), dtype=np.int8)

    def __getitem__(self, coords):
        """
        Returns the value at a specific location on the board
        :param row: row to check
        :param col: column to check
        """

        row, col = coords
        return self.board[row, col]

    def _get_next_open_row(self, col):
        """
        Returns the lowest available row in a column
        :param col: column to check

        :return: row to drop the piece
        """

        return self.ROWS - 1 - np.count_nonzero(self.board, axis=0)[col]

    def check_draw(self):
        """
        Checks if the board is full
        """

        return len(self.get_valid_locations()) == 0

    def check_winner(self):
        """
        Checks if a player has won the game

        :return:
            0: No winner
            1: Player 1 wins
            2: Player 2 wins
        """

        def check_line(start_row, start_col, delta_row, delta_col):
            """
            Check a line of k cells starting from (start_row, start_col) in a given direction.

            :param start_row: Starting row
            :param start_col: Starting column
            :param delta_row: Row increment direction
            :param delta_col: Column increment direction
            :return: True if a winning line is found, False otherwise
            """

            piece = self.board[start_row, start_col]

            if piece == 0:
                return 0  # Empty cell can't form a line

            for i in range(1, self.k):
                r, c = start_row + i * delta_row, start_col + i * delta_col
                if not (0 <= r < self.ROWS and 0 <= c < self.COLS):  # Boundary check
                    return 0
                if self.board[r, c] != piece:
                    return 0
            return piece

        # Check for win conditions in all directions
        for row in range(self.ROWS):
            for col in range(self.COLS):
                winner = (
                    check_line(row, col, 0, 1) or  # Horizontal
                    check_line(row, col, 1, 0) or  # Vertical
                    check_line(row, col, 1, 1) or  # Positive diagonal
                    check_line(row, col, 1, -1)    # Negative diagonal
                )

                if winner:
                    return winner

        # No winner
        return 0

    def add_piece(self, col, piece):
        """
        Drops a piece into the board
        :param col: column to drop the piece
        :param piece: piece to drop
        """

        row = self._get_next_open_row(col)
        self.board[row, col] = piece
        return row, col

    def get_valid_locations(self):
        """
        Returns a list of valid locations to drop a piece
        """

        valid_locations = []
        for col in range(self.COLS):
            if self.is_valid(col):
                valid_locations.append(col)
        return valid_locations

    def is_terminal(self):
        """
        Checks if the game is in a terminal state (win or full board).

        :return: True if the game is in a terminal state, False otherwise
        """

        # Check for a winner
        winner = self.check_winner()
        if winner:
            return (True, winner)

        # Check for a draw
        if self.check_draw():
            return (True, 0)

        return (False, 0)

    def is_valid(self, col):
        """
        Checks if a column is valid to drop a piece
        :param col: column to check

        :return: True if the column is valid, False otherwise
        """

        if col < 0 or col >= self.COLS:
            # Column is out of bounds
            return False

        # If the top row is empty, there is space to drop a piece
        return self.board[0, col] == 0

    def remove_piece(self, row, col):
        """
        Resets a piece on the board
        :param row: row to reset
        :param col: column to reset
        """

        self.board[row, col] = 0


class Game:

    def __init__(self, player1=None, player2=None, m=7, n=6, k=4):
        """
        Initialises the game with the board size and number of pieces in a row to win
        :param m: number of columns
        :param n: number of rows
        :param k: number of pieces in a row to win

        For example, Connect-4 is a 7x6 board with 4 pieces in a row to win
        """

        self.m = m  # Cols
        self.n = n  # rows
        self.k = k  # num in a row to win

        self.player1 = player1  # Max player
        self.player2 = player2  # Min player

        self.board = self.initialise_game()

    def initialise_game(self):
        """
        Initialises the game board
        """

        return Board(self.m, self.n, self.k)

    def draw_board(self):
        """
        Draws the game board
        """

        # Define ANSI color codes
        EMPTY = "   "  # Empty cell
        PLAYER1 = "\033[31m X \033[0m"  # Red for Player 1
        PLAYER2 = "\033[33m O \033[0m"  # Yellow for Player 2

        # Print column numbers
        col_numbers = EMPTY.join([f"{i+1}" for i in range(self.m)])
        print(f"  {col_numbers}")

        for row in range(self.n):
            line = ''
            for col in range(self.m):
                if self.board[row, col] == 0:
                    visual = EMPTY
                if self.board[row, col] == self.player1.piece:
                    visual = PLAYER1
                if self.board[row, col] == self.player2.piece:
                    visual = PLAYER2
                line += f"{visual}|"
            print(f"|{line}")
        print(f"\n")

    def play(self, quiet=False, record_stats=False):
        """
        Main game loop
        """

        print(f"Playing: Connect-{self.k} on {self.m}x{self.n} grid")

        # Show empty board
        if not quiet:
            self.draw_board()

        cur_player, next_player = self.player1, self.player2

        time_arr = []
        move_arr = []

        # Begin game loop
        game_over, winner = self.board.is_terminal()
        while not game_over:
            # Current player selects action and makes move
            start_time = time.time()
            col = cur_player.select_move(self.board)
            timer = time.time() - start_time

            if record_stats and cur_player.max_player:
                time_arr.append(timer)
                move_arr.append(cur_player.counter)

            self.board.add_piece(col, cur_player.piece)
            if not quiet:
                self.draw_board()

            # Players swap turns
            cur_player, next_player = next_player, cur_player
            game_over, winner = self.board.is_terminal()

        if not quiet:
            print(f"Player {winner} wins!") if winner else print("It's a draw!")

        return winner, time_arr, move_arr


if __name__ == "__main__":
    pass

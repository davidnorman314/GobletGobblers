"""Classes representing the state of a game."""

from enum import Enum

import numpy as np
import copy


class Piece(Enum):
    ORANGE_BIG = 0x04
    ORANGE_MEDIUM = 0x02
    ORANGE_SMALL = 0x01
    BLUE_BIG = 0x40
    BLUE_MEDIUM = 0x20
    BLUE_SMALL = 0x10


class Player(Enum):
    ORANGE = 0x07
    BLUE = 0x70


class Source(Enum):
    ORANGE = 0x07
    BLUE = 0x70


class State:
    _board: np.ndarray
    """The board. This is an array of size nine, one for each square of the board. The array is np.int8, with
    each the first six bits of the value indicating if the given piece is in the square. The bit to piece mapping 
    is given by the Pieces enum."""

    to_play: Player
    """Which player should play next."""

    symmetries = None

    win_indices: list[list[int]] = None

    _cannot_place_pieces: np.ndarray = None

    _cannot_move_pieces: np.ndarray = None

    _pieces_by_player: dict = None

    def __init__(
        self,
        to_play: Player,
        initial_board: np.ndarray = None,
        pieces: list[tuple[int, int, Piece]] = None,
    ):
        self.to_play = to_play

        # Initilize the symmetries, if necessary
        if self.symmetries == None:
            self.create_symmetries()

        if initial_board is None:
            initial_board = np.zeros(shape=9, dtype=np.int8)

        # Initialize _pieces_by_player
        self._pieces_by_player = {
            Player.BLUE: [Piece.BLUE_BIG, Piece.BLUE_MEDIUM, Piece.BLUE_SMALL],
            Player.ORANGE: [Piece.ORANGE_BIG, Piece.ORANGE_MEDIUM, Piece.ORANGE_SMALL],
        }

        # Initialize _cannot_place_pieces
        self._cannot_place_pieces = np.zeros(
            Player.BLUE.value + Player.ORANGE.value + 1, dtype=np.int8
        )
        self._cannot_place_pieces[Piece.ORANGE_BIG.value] = (
            Piece.BLUE_BIG.value + Piece.ORANGE_BIG.value
        )
        self._cannot_place_pieces[Piece.ORANGE_MEDIUM.value] = (
            Piece.BLUE_BIG.value
            + Piece.ORANGE_BIG.value
            + Piece.BLUE_MEDIUM.value
            + Piece.ORANGE_MEDIUM.value
        )
        self._cannot_place_pieces[Piece.ORANGE_SMALL.value] = (
            Piece.BLUE_BIG.value
            + Piece.ORANGE_BIG.value
            + Piece.BLUE_MEDIUM.value
            + Piece.ORANGE_MEDIUM.value
            + Piece.BLUE_SMALL.value
            + Piece.ORANGE_SMALL.value
        )
        self._cannot_place_pieces[Piece.BLUE_BIG.value] = (
            Piece.BLUE_BIG.value + Piece.ORANGE_BIG.value
        )
        self._cannot_place_pieces[Piece.BLUE_MEDIUM.value] = (
            Piece.BLUE_BIG.value
            + Piece.ORANGE_BIG.value
            + Piece.BLUE_MEDIUM.value
            + Piece.ORANGE_MEDIUM.value
        )
        self._cannot_place_pieces[Piece.BLUE_SMALL.value] = (
            Piece.BLUE_BIG.value
            + Piece.ORANGE_BIG.value
            + Piece.BLUE_MEDIUM.value
            + Piece.ORANGE_MEDIUM.value
            + Piece.BLUE_SMALL.value
            + Piece.ORANGE_SMALL.value
        )

        # Initialize _cannot_move_pieces
        self._cannot_move_pieces = np.zeros(
            Player.BLUE.value + Player.ORANGE.value + 1, dtype=np.int8
        )
        self._cannot_move_pieces[Piece.ORANGE_BIG.value] = 0
        self._cannot_move_pieces[Piece.ORANGE_MEDIUM.value] = (
            Piece.BLUE_BIG.value + Piece.ORANGE_BIG.value
        )
        self._cannot_move_pieces[Piece.ORANGE_SMALL.value] = (
            Piece.BLUE_BIG.value
            + Piece.ORANGE_BIG.value
            + Piece.BLUE_MEDIUM.value
            + Piece.ORANGE_MEDIUM.value
        )
        self._cannot_move_pieces[Piece.BLUE_BIG.value] = 0
        self._cannot_move_pieces[Piece.BLUE_MEDIUM.value] = (
            Piece.BLUE_BIG.value + Piece.ORANGE_BIG.value
        )
        self._cannot_move_pieces[Piece.BLUE_SMALL.value] = (
            Piece.BLUE_BIG.value
            + Piece.ORANGE_BIG.value
            + Piece.BLUE_MEDIUM.value
            + Piece.ORANGE_MEDIUM.value
        )

        # Initialize win_indices, if necessary
        if self.win_indices == None:
            self.win_indices = [
                # Diagonals
                [3 * 0 + 0, 3 * 1 + 1, 3 * 2 + 2],
                [3 * 2 + 0, 3 * 1 + 1, 3 * 0 + 2],
                # Rows
                [3 * 0 + 0, 3 * 0 + 1, 3 * 0 + 2],
                [3 * 1 + 0, 3 * 1 + 1, 3 * 1 + 2],
                [3 * 2 + 0, 3 * 2 + 1, 3 * 2 + 2],
                # Columns
                [3 * 0 + 0, 3 * 1 + 0, 3 * 2 + 0],
                [3 * 0 + 1, 3 * 1 + 1, 3 * 2 + 1],
                [3 * 0 + 2, 3 * 1 + 2, 3 * 2 + 2],
            ]

        # Add the pieces to the board
        if pieces is not None:
            for row, col, piece in pieces:
                initial_board[3 * row + col] |= piece.value

        # Check all the boards that equivalent by symmetery and pick the cannonical one.
        # We don't need to create an equivalent board using the identity.
        equivalent_boards = []
        equivalent_boards.append(initial_board)
        for i in range(1, len(self.symmetries)):
            symmetry = self.symmetries[i]

            equivalent_board = np.zeros(shape=9, dtype=np.int8)
            for cell in range(9):
                equivalent_board[cell] = initial_board[symmetry[cell]]

            equivalent_boards.append(equivalent_board)

        largest = None
        for board in equivalent_boards:
            if largest is None:
                largest = board
            elif self._lexographic_greater_than(board, largest):
                largest = board

        # Save off the cannonical board
        self._board = largest

    def play(
        self, piece: Piece, from_row: int, from_col: int, to_row: int, to_col: int
    ) -> "State":
        """Plays a piece. If from_row and from_col are None, then the piece
        is taken from the players hand and put on the board."""

        # From_row and from_col must be either both None or neither None
        assert (from_row is None) == (from_col is None)

        # Get the next player
        next_player = Player.ORANGE if self.to_play == Player.BLUE else Player.BLUE

        # Create the board for the new state
        initial_board = self._board.copy()

        if from_row is not None:
            assert initial_board[3 * from_row + from_col] & piece.value != 0
            initial_board[3 * from_row + from_col] &= ~piece.value

        return State(
            to_play=next_player,
            initial_board=initial_board,
            pieces=[(to_row, to_col, piece)],
        )

    def is_win(self) -> Player:
        """Checks to see if a state is a win for a player. If it is a win, the
        winner is returned. Otherwise None is returned."""

        # Calculate who owns each square of the board
        owner = np.zeros(shape=9, dtype=np.int8)
        for i in range(9):
            square_state = self._board[i]
            orange_state = square_state & Player.ORANGE.value
            blue_state = (square_state & Player.BLUE.value) >> 3

            if orange_state > blue_state:
                owner[i] = Player.ORANGE.value
            elif orange_state < blue_state:
                owner[i] = Player.BLUE.value

        # Check each possible win
        blue_win = False
        orange_win = False
        for indices in self.win_indices:
            if owner[indices[0]] == owner[indices[1]] == owner[indices[2]]:
                if owner[indices[0]] == Player.ORANGE.value:
                    orange_win = True
                elif owner[indices[0]] == Player.BLUE.value:
                    blue_win = True

        if blue_win and orange_win:
            return Player.BLUE if self.to_play == Player.ORANGE else Player.ORANGE
        elif blue_win:
            return Player.BLUE
        elif orange_win:
            return Player.ORANGE
        else:
            return None

    def valid_moves(self):
        """Returns all valid moves in the current state."""

        # Find the pieces in the players hand
        player_pieces = self._pieces_by_player[self.to_play]
        piece_counts = [0] * 3

        for row in range(3):
            for col in range(3):
                current_pieces = self._board[3 * row + col]
                for i in range(len(player_pieces)):
                    if current_pieces & player_pieces[i].value > 0:
                        piece_counts[i] += 1

        # Moving pieces from the players hand onto the board.
        ret = []
        for piece, piece_count in zip(player_pieces, piece_counts):
            if piece_count == 2:
                continue

            for row in range(3):
                for col in range(3):
                    current_pieces = self._board[3 * row + col]
                    if (current_pieces & self._cannot_place_pieces[piece.value]) == 0:
                        ret.append((piece, None, None, row, col))

        # Moving pieces on the board to another square
        for from_row in range(3):
            for from_col in range(3):
                from_pieces = self._board[3 * from_row + from_col]
                for piece in player_pieces:
                    if from_pieces & piece.value == 0:
                        continue

                    if (from_pieces & self._cannot_move_pieces[piece.value]) > 0:
                        continue

                    for to_row in range(3):
                        for to_col in range(3):
                            if to_row == from_row and to_col == from_col:
                                continue

                            to_pieces = self._board[3 * to_row + to_col]
                            if (
                                to_pieces & self._cannot_place_pieces[piece.value]
                            ) == 0:
                                ret.append((piece, from_row, from_col, to_row, to_col))

        return ret

    def __eq__(self, o):
        assert isinstance(o, State)

        return np.array_equal(self._board, o._board)

    def __nq__(self, o):
        return not self.__eq__(o)

    def _lexographic_greater_than(self, b1: np.ndarray, b2: np.ndarray):
        for x, y in zip(b1, b2):
            if x == y:
                continue

            return x > y

        return False

    def create_symmetries(self):
        # The symmetries can be generated from a rotation and a diagonal reflection
        identity = [0, 1, 2, 3, 4, 5, 6, 7, 8]

        rotate = [0] * 9
        rotate[3 * 0 + 0] = 3 * 0 + 2
        rotate[3 * 0 + 1] = 3 * 1 + 2
        rotate[3 * 0 + 2] = 3 * 2 + 2
        rotate[3 * 1 + 0] = 3 * 0 + 1
        rotate[3 * 1 + 1] = 3 * 1 + 1
        rotate[3 * 1 + 2] = 3 * 2 + 1
        rotate[3 * 2 + 0] = 3 * 0 + 0
        rotate[3 * 2 + 1] = 3 * 1 + 0
        rotate[3 * 2 + 2] = 3 * 2 + 0

        reflect = [0] * 9
        reflect[3 * 0 + 0] = 3 * 0 + 0
        reflect[3 * 0 + 1] = 3 * 1 + 0
        reflect[3 * 0 + 2] = 3 * 2 + 0
        reflect[3 * 1 + 0] = 3 * 0 + 1
        reflect[3 * 1 + 1] = 3 * 1 + 1
        reflect[3 * 1 + 2] = 3 * 2 + 1
        reflect[3 * 2 + 0] = 3 * 0 + 2
        reflect[3 * 2 + 1] = 3 * 1 + 2
        reflect[3 * 2 + 2] = 3 * 2 + 2

        # There are eight symmetries:
        #  - The identity
        #  - Three rotations
        #  - One reflection
        #  - Three combinations of rotation and reflection
        self.symmetries = []

        r1 = identity
        self.symmetries.append(r1)

        r2 = self._mult_symmetry(rotate, r1)
        self.symmetries.append(r2)

        r3 = self._mult_symmetry(rotate, r2)
        self.symmetries.append(r3)

        r4 = self._mult_symmetry(rotate, r3)
        self.symmetries.append(r4)

        if False:
            for i in range(len(self.symmetries)):
                self._print_symmetry(self.symmetries[i])

        # The next four include a reflection
        for i in range(4):
            sym = self._mult_symmetry(self.symmetries[i], reflect)
            self.symmetries.append(sym)

        # Validate that we have eight distinct symmetries.
        assert len(self.symmetries) == 8

        for i in range(len(self.symmetries)):
            for j in range(len(self.symmetries)):
                if i == j:
                    continue

                if self.symmetries[i] == self.symmetries[j]:
                    print(f"Equal symmetries {i} {j}")
                    print(self.symmetries[i])
                    print(self.symmetries[j])

                assert self.symmetries[i] != self.symmetries[j]

    def _mult_symmetry(self, s1: list, s2: list):
        result = [0] * 9

        for i in range(9):
            result[i] = s2[s1[i]]

        return result

    def _print_symmetry(self, sym: list):
        base = [0, 3, 6, 1, 4, 7, 2, 5, 8]

        for i in range(3):
            if i == 1:
                mid = "->"
            else:
                mid = "  "

            a = base[3 * 0 + i]
            b = base[3 * 1 + i]
            c = base[3 * 2 + i]

            x = sym[base[3 * 0 + i]]
            y = sym[base[3 * 1 + i]]
            z = sym[base[3 * 2 + i]]
            print(f"{a} {b} {c} {mid} {x} {y} {z}")

        print("")

    def __repr__(self):
        return str(self._board)

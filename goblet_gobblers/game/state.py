"""Classes representing the state of a game."""

from enum import Enum

import numpy as np


class Piece(Enum):
    ORANGE_BIG = 0x01
    ORANGE_MEDIUM = 0x02
    ORANGE_SMALL = 0x04
    BLUE_BIG = 0x08
    BLUE_MEDIUM = 0x10
    BLUE_SMALL = 0x20


class State:

    _board: np.ndarray
    """The board. This is an array of size nine, one for each square of the board. The array is np.int8, with
    each the first six bits of the value indicating if the given piece is in the square. The bit to piece mapping 
    is given by the Pieces enum."""

    symmetries = None

    def __init__(self, pieces: list[tuple[int, int, Piece]] = None):
        # Initilize the symmetries, if necessary
        if self.symmetries == None:
            self.create_symmetries()

        initial_board = np.zeros(shape=9, dtype=np.int8)

        # Add the pieces to the board
        for x, y, piece in pieces:
            initial_board[3 * x + y] = piece.value

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

        smallest = None
        for board in equivalent_boards:
            if smallest is None:
                smallest = board
            elif self._lexographic_less_than(board, smallest):
                smallest = board

        # Save off the cannonical board
        self._board = smallest

    def __eq__(self, o):
        assert isinstance(o, State)

        return np.array_equal(self._board, o._board)

    def __nq__(self, o):
        return not self.__eq__(o)

    def _lexographic_less_than(self, b1: np.ndarray, b2: np.ndarray):
        for x, y in zip(b1, b2):
            if x == y:
                continue

            return x < y

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

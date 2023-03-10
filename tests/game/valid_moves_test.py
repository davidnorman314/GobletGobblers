"""Tests for the game State."""

from goblet_gobblers.game.state import State, Piece, Player


def moves_for_piece(piece: Piece, all_moves: list[tuple]):
    return [move for move in all_moves if move[0] == piece]


def moves_from_hand(all_moves: list[tuple]):
    return [move for move in all_moves if move[1] == None and move[2] == None]


def moves_from_board(all_moves: list[tuple]):
    return [move for move in all_moves if move[1] is not None or move[2] is not None]


def moves_to_square(to_row, to_col, all_moves: list[tuple]):
    return [move for move in all_moves if move[3] == to_row and move[4] == to_col]


def moves_from_square(from_row, from_col, all_moves: list[tuple]):
    return [move for move in all_moves if move[1] == from_row and move[1] == from_col]


def from_square(all_moves: list[tuple]):
    return [(move[1], move[2]) for move in all_moves]


def to_square(all_moves: list[tuple]):
    return [(move[3], move[4]) for move in all_moves]


def test_move_from_hand():
    """Test moves from the hand onto the board."""

    # Test an empty board
    empty = State(Player.ORANGE, pieces=[])
    all_moves = empty.valid_moves()

    piece_moves = moves_for_piece(Piece.ORANGE_BIG, all_moves)

    assert len(moves_from_board(piece_moves)) == 0

    assert sorted(to_square(moves_from_hand(piece_moves))) == [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 1),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2),
    ]

    # Test a board with various pieces. Here orange plays next.
    empty = State(
        Player.ORANGE,
        pieces=[
            (0, 0, Piece.BLUE_BIG),
            (0, 1, Piece.BLUE_MEDIUM),
            (0, 2, Piece.BLUE_SMALL),
            (1, 0, Piece.ORANGE_BIG),
            (1, 1, Piece.ORANGE_MEDIUM),
            (1, 2, Piece.ORANGE_SMALL),
        ],
    )
    all_moves = empty.valid_moves()

    empty_squares = [(2, 0), (2, 1), (2, 2)]

    piece_moves = moves_for_piece(Piece.ORANGE_BIG, all_moves)
    assert sorted(to_square(moves_from_hand(piece_moves))) == [
        (0, 1),
        (0, 2),
        (1, 1),
        (1, 2),
        *empty_squares,
    ]

    piece_moves = moves_for_piece(Piece.ORANGE_MEDIUM, all_moves)
    assert sorted(to_square(moves_from_hand(piece_moves))) == [
        (0, 2),
        (1, 2),
        *empty_squares,
    ]

    piece_moves = moves_for_piece(Piece.ORANGE_SMALL, all_moves)
    assert sorted(to_square(moves_from_hand(piece_moves))) == [
        *empty_squares,
    ]

    # Test a board with various pieces. Here blue plays next.
    empty = State(
        Player.BLUE,
        pieces=[
            (0, 0, Piece.BLUE_BIG),
            (0, 1, Piece.BLUE_MEDIUM),
            (0, 2, Piece.BLUE_SMALL),
            (1, 0, Piece.ORANGE_BIG),
            (1, 1, Piece.ORANGE_MEDIUM),
            (1, 2, Piece.ORANGE_SMALL),
        ],
    )
    all_moves = empty.valid_moves()

    empty_squares = [(2, 0), (2, 1), (2, 2)]

    piece_moves = moves_for_piece(Piece.BLUE_BIG, all_moves)
    assert sorted(to_square(moves_from_hand(piece_moves))) == [
        (0, 1),
        (0, 2),
        (1, 1),
        (1, 2),
        *empty_squares,
    ]

    piece_moves = moves_for_piece(Piece.BLUE_MEDIUM, all_moves)
    assert sorted(to_square(moves_from_hand(piece_moves))) == [
        (0, 2),
        (1, 2),
        *empty_squares,
    ]

    piece_moves = moves_for_piece(Piece.BLUE_SMALL, all_moves)
    assert sorted(to_square(moves_from_hand(piece_moves))) == [
        *empty_squares,
    ]

    # Test where both copies of the piece are on the board
    empty = State(
        Player.ORANGE,
        pieces=[
            (1, 0, Piece.ORANGE_BIG),
            (1, 1, Piece.ORANGE_BIG),
        ],
    )
    all_moves = empty.valid_moves()

    piece_moves = moves_from_hand(moves_for_piece(Piece.ORANGE_BIG, all_moves))
    assert len(piece_moves) == 0

    piece_moves = moves_from_hand(moves_for_piece(Piece.ORANGE_MEDIUM, all_moves))
    assert len(piece_moves) > 0

    empty = State(
        Player.ORANGE,
        pieces=[
            (1, 0, Piece.ORANGE_MEDIUM),
            (1, 1, Piece.ORANGE_MEDIUM),
        ],
    )
    all_moves = empty.valid_moves()

    piece_moves = moves_from_hand(moves_for_piece(Piece.ORANGE_MEDIUM, all_moves))
    assert len(piece_moves) == 0

    piece_moves = moves_from_hand(moves_for_piece(Piece.ORANGE_BIG, all_moves))
    assert len(piece_moves) > 0

    # Test where one piece of each type is on the board
    empty = State(
        Player.ORANGE,
        pieces=[
            (0, 0, Piece.ORANGE_BIG),
            (0, 0, Piece.ORANGE_MEDIUM),
            (0, 0, Piece.ORANGE_SMALL),
        ],
    )
    all_moves = empty.valid_moves()

    piece_moves = moves_for_piece(Piece.ORANGE_BIG, all_moves)
    assert len(piece_moves) > 0

    piece_moves = moves_for_piece(Piece.ORANGE_MEDIUM, all_moves)
    assert len(piece_moves) > 0

    piece_moves = moves_for_piece(Piece.ORANGE_SMALL, all_moves)
    assert len(piece_moves) > 0

    # Test where all pieces are on the board
    empty = State(
        Player.ORANGE,
        pieces=[
            (0, 0, Piece.ORANGE_BIG),
            (1, 1, Piece.ORANGE_BIG),
            (0, 0, Piece.ORANGE_MEDIUM),
            (1, 1, Piece.ORANGE_MEDIUM),
            (0, 0, Piece.ORANGE_SMALL),
            (1, 1, Piece.ORANGE_SMALL),
        ],
    )
    all_moves = empty.valid_moves()

    piece_moves = moves_from_hand(moves_for_piece(Piece.ORANGE_BIG, all_moves))
    assert len(piece_moves) == 0

    piece_moves = moves_from_hand(moves_for_piece(Piece.ORANGE_MEDIUM, all_moves))
    assert len(piece_moves) == 0

    piece_moves = moves_from_hand(moves_for_piece(Piece.ORANGE_SMALL, all_moves))
    assert len(piece_moves) == 0


def test_move_piece_on_board():
    """Test moves of a piece on the board to another place."""

    # Test a board with one piece
    state = State(Player.ORANGE, pieces=[(0, 0, Piece.ORANGE_BIG)])
    all_moves = state.valid_moves()

    piece_moves = moves_for_piece(Piece.ORANGE_BIG, all_moves)

    assert sorted(to_square(moves_from_board(piece_moves))) == [
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 1),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2),
    ]

    # Test a board with two identical pieces
    state = State(
        Player.ORANGE, pieces=[(0, 0, Piece.ORANGE_BIG), (2, 2, Piece.ORANGE_BIG)]
    )
    all_moves = state.valid_moves()

    piece_moves = moves_for_piece(Piece.ORANGE_BIG, all_moves)

    assert sorted(moves_from_board(piece_moves)) == [
        (Piece.ORANGE_BIG, 0, 0, 0, 1),
        (Piece.ORANGE_BIG, 0, 0, 0, 2),
        (Piece.ORANGE_BIG, 0, 0, 1, 0),
        (Piece.ORANGE_BIG, 0, 0, 1, 1),
        (Piece.ORANGE_BIG, 0, 0, 1, 2),
        (Piece.ORANGE_BIG, 0, 0, 2, 0),
        (Piece.ORANGE_BIG, 0, 0, 2, 1),
        (Piece.ORANGE_BIG, 2, 2, 0, 1),
        (Piece.ORANGE_BIG, 2, 2, 0, 2),
        (Piece.ORANGE_BIG, 2, 2, 1, 0),
        (Piece.ORANGE_BIG, 2, 2, 1, 1),
        (Piece.ORANGE_BIG, 2, 2, 1, 2),
        (Piece.ORANGE_BIG, 2, 2, 2, 0),
        (Piece.ORANGE_BIG, 2, 2, 2, 1),
    ]

    # Test moving a big piece on a board with other pieces. Here orange moves first.
    state = State(
        Player.ORANGE,
        pieces=[
            (0, 0, Piece.BLUE_BIG),
            (0, 1, Piece.BLUE_MEDIUM),
            (0, 2, Piece.BLUE_SMALL),
            (1, 0, Piece.ORANGE_BIG),
            (1, 1, Piece.ORANGE_MEDIUM),
            (1, 2, Piece.ORANGE_SMALL),
        ],
    )
    empty_squares = [(2, 0), (2, 1), (2, 2)]
    all_moves = state.valid_moves()

    piece_moves = moves_for_piece(Piece.ORANGE_BIG, all_moves)
    assert sorted(to_square(moves_from_board(piece_moves))) == [
        (0, 1),
        (0, 2),
        (1, 1),
        (1, 2),
        *empty_squares,
    ]

    piece_moves = moves_for_piece(Piece.ORANGE_MEDIUM, all_moves)
    assert sorted(to_square(moves_from_board(piece_moves))) == [
        (0, 2),
        (1, 2),
        *empty_squares,
    ]

    piece_moves = moves_for_piece(Piece.ORANGE_SMALL, all_moves)
    assert sorted(to_square(moves_from_board(piece_moves))) == [
        *empty_squares,
    ]

    # Test moving a big piece on a board with other pieces. Here blue moves first.
    state = State(
        Player.BLUE,
        pieces=[
            (0, 0, Piece.BLUE_BIG),
            (0, 1, Piece.BLUE_MEDIUM),
            (0, 2, Piece.BLUE_SMALL),
            (1, 0, Piece.ORANGE_BIG),
            (1, 1, Piece.ORANGE_MEDIUM),
            (1, 2, Piece.ORANGE_SMALL),
        ],
    )
    empty_squares = [(2, 0), (2, 1), (2, 2)]
    all_moves = state.valid_moves()

    piece_moves = moves_for_piece(Piece.BLUE_BIG, all_moves)
    assert sorted(to_square(moves_from_board(piece_moves))) == [
        (0, 1),
        (0, 2),
        (1, 1),
        (1, 2),
        *empty_squares,
    ]

    piece_moves = moves_for_piece(Piece.BLUE_MEDIUM, all_moves)
    assert sorted(to_square(moves_from_board(piece_moves))) == [
        (0, 2),
        (1, 2),
        *empty_squares,
    ]

    piece_moves = moves_for_piece(Piece.BLUE_SMALL, all_moves)
    assert sorted(to_square(moves_from_board(piece_moves))) == [
        *empty_squares,
    ]

    # Test moving a piece under another piece. Here the piece is medium.
    state = State(
        Player.BLUE,
        pieces=[
            (0, 0, Piece.BLUE_MEDIUM),
            (0, 1, Piece.BLUE_MEDIUM),
            (0, 0, Piece.BLUE_BIG),
            (0, 1, Piece.ORANGE_BIG),
        ],
    )
    empty_squares = [(2, 0), (2, 1), (2, 2)]
    all_moves = state.valid_moves()
    piece_moves = moves_for_piece(Piece.BLUE_MEDIUM, all_moves)
    assert len(piece_moves) == 0

    # Test moving a piece under another piece. Here the piece is small.
    state = State(
        Player.BLUE,
        pieces=[
            (0, 0, Piece.BLUE_SMALL),
            (0, 1, Piece.BLUE_SMALL),
            (0, 0, Piece.BLUE_BIG),
            (0, 1, Piece.ORANGE_BIG),
        ],
    )
    empty_squares = [(2, 0), (2, 1), (2, 2)]
    all_moves = state.valid_moves()
    piece_moves = moves_for_piece(Piece.BLUE_SMALL, all_moves)
    assert len(piece_moves) == 0

    state = State(
        Player.BLUE,
        pieces=[
            (0, 0, Piece.BLUE_SMALL),
            (0, 1, Piece.BLUE_SMALL),
            (0, 0, Piece.BLUE_MEDIUM),
            (0, 1, Piece.ORANGE_MEDIUM),
        ],
    )
    empty_squares = [(2, 0), (2, 1), (2, 2)]
    all_moves = state.valid_moves()
    piece_moves = moves_for_piece(Piece.BLUE_SMALL, all_moves)
    assert len(piece_moves) == 0

    # Test moving a piece on top of another piece. Here the piece is medium.
    state = State(
        Player.BLUE,
        pieces=[
            (0, 0, Piece.BLUE_MEDIUM),
            (0, 1, Piece.BLUE_MEDIUM),
            (0, 0, Piece.BLUE_SMALL),
            (0, 1, Piece.ORANGE_SMALL),
        ],
    )
    all_moves = state.valid_moves()
    from_squares = from_square(moves_for_piece(Piece.BLUE_MEDIUM, all_moves))
    assert (0, 0) in from_squares
    assert (0, 1) in from_squares

    # Test moving a piece on top of another piece. Here the piece is big.
    state = State(
        Player.BLUE,
        pieces=[
            (0, 0, Piece.BLUE_BIG),
            (0, 1, Piece.BLUE_BIG),
            (0, 0, Piece.BLUE_SMALL),
            (0, 1, Piece.ORANGE_MEDIUM),
        ],
    )
    all_moves = state.valid_moves()
    from_squares = from_square(moves_for_piece(Piece.BLUE_BIG, all_moves))
    assert (0, 0) in from_squares
    assert (0, 1) in from_squares

"""Tests for the game State."""

from goblet_gobblers.game.state import State, Piece, Player


def test_state():
    """Test basic state operations"""
    state1 = State(Player.ORANGE, pieces=[(0, 0, Piece.ORANGE_BIG)])
    assert state1.to_play == Player.ORANGE

    state2 = State(Player.BLUE, pieces=[(0, 0, Piece.ORANGE_BIG)])
    assert state2.to_play == Player.BLUE

def test_state_symmetry():
    """Test that the State object takes into account board symmetries, i.e., each
    board is converted to a cannonical equivalent board."""

    # Check where there is a single piece in a corner
    state_big_1 = State(Player.ORANGE, pieces=[(0, 0, Piece.ORANGE_BIG)])
    state_big_2 = State(Player.ORANGE, pieces=[(2, 0, Piece.ORANGE_BIG)])
    state_big_3 = State(Player.ORANGE, pieces=[(0, 2, Piece.ORANGE_BIG)])
    state_big_4 = State(Player.ORANGE, pieces=[(2, 2, Piece.ORANGE_BIG)])

    state_med_1 = State(Player.ORANGE, pieces=[(0, 0, Piece.ORANGE_MEDIUM)])
    state_med_2 = State(Player.ORANGE, pieces=[(2, 0, Piece.ORANGE_MEDIUM)])
    state_med_3 = State(Player.ORANGE, pieces=[(0, 2, Piece.ORANGE_MEDIUM)])
    state_med_4 = State(Player.ORANGE, pieces=[(2, 2, Piece.ORANGE_MEDIUM)])

    assert state_big_1 == state_big_2
    assert state_big_1 == state_big_3
    assert state_big_1 == state_big_4

    assert state_med_1 == state_med_2
    assert state_med_1 == state_med_3
    assert state_med_1 == state_med_4

    assert state_big_1 != state_med_1

    # Test when three corners are occupied by different pieces
    state_big_1 = State(
        to_play = Player.ORANGE,
        pieces=[
            (0, 0, Piece.ORANGE_MEDIUM),
            (1, 0, Piece.ORANGE_SMALL),
            (0, 1, Piece.ORANGE_BIG),
        ]
    )
    state_big_2 = State(
        to_play = Player.ORANGE,
        pieces=[
            (0, 0, Piece.ORANGE_MEDIUM),
            (0, 1, Piece.ORANGE_SMALL),
            (1, 0, Piece.ORANGE_BIG),
        ]
    )
    state_big_3 = State(
        to_play = Player.ORANGE,
        pieces=[
            (2, 0, Piece.ORANGE_MEDIUM),
            (1, 0, Piece.ORANGE_SMALL),
            (2, 1, Piece.ORANGE_BIG),
        ]
    )
    state_big_4 = State(
        to_play = Player.ORANGE,
        pieces=[
            (2, 0, Piece.ORANGE_MEDIUM),
            (2, 1, Piece.ORANGE_SMALL),
            (1, 0, Piece.ORANGE_BIG),
        ]
    )
    state_big_5 = State(
        to_play = Player.ORANGE,
        pieces=[
            (0, 2, Piece.ORANGE_MEDIUM),
            (0, 1, Piece.ORANGE_SMALL),
            (1, 2, Piece.ORANGE_BIG),
        ]
    )
    state_big_6 = State(
        to_play = Player.ORANGE,
        pieces=[
            (0, 2, Piece.ORANGE_MEDIUM),
            (1, 2, Piece.ORANGE_SMALL),
            (0, 1, Piece.ORANGE_BIG),
        ]
    )
    state_big_7 = State(
        to_play = Player.ORANGE,
        pieces=[
            (2, 2, Piece.ORANGE_MEDIUM),
            (1, 2, Piece.ORANGE_SMALL),
            (2, 1, Piece.ORANGE_BIG),
        ]
    )
    state_big_8 = State(
        to_play = Player.ORANGE,
        pieces=[
            (2, 2, Piece.ORANGE_MEDIUM),
            (2, 1, Piece.ORANGE_SMALL),
            (1, 2, Piece.ORANGE_BIG),
        ]
    )

    assert state_big_1 == state_big_2
    assert state_big_1 == state_big_3
    assert state_big_1 == state_big_4
    assert state_big_1 == state_big_5
    assert state_big_1 == state_big_6
    assert state_big_1 == state_big_7
    assert state_big_1 == state_big_8

    state_big_a = State(
        to_play = Player.ORANGE,
        pieces=[
            (2, 2, Piece.ORANGE_SMALL),
            (2, 1, Piece.ORANGE_MEDIUM),
            (1, 2, Piece.ORANGE_BIG),
        ]
    )

    assert state_big_1 != state_big_a

    # Test where there is one side piece
    state_big_1 = State(Player.ORANGE, pieces=[(1, 0, Piece.ORANGE_BIG)])
    state_big_2 = State(Player.ORANGE, pieces=[(0, 1, Piece.ORANGE_BIG)])
    state_big_3 = State(Player.ORANGE, pieces=[(1, 2, Piece.ORANGE_BIG)])
    state_big_4 = State(Player.ORANGE, pieces=[(2, 1, Piece.ORANGE_BIG)])

    state_med_1 = State(Player.ORANGE, pieces=[(1, 0, Piece.ORANGE_MEDIUM)])
    state_med_2 = State(Player.ORANGE, pieces=[(0, 1, Piece.ORANGE_MEDIUM)])
    state_med_3 = State(Player.ORANGE, pieces=[(1, 2, Piece.ORANGE_MEDIUM)])
    state_med_4 = State(Player.ORANGE, pieces=[(2, 1, Piece.ORANGE_MEDIUM)])

    assert state_big_1 == state_big_2
    assert state_big_1 == state_big_3
    assert state_big_1 == state_big_4

    assert state_med_1 == state_med_2
    assert state_med_1 == state_med_3
    assert state_med_1 == state_med_4

    assert state_big_1 != state_med_1

    # Test when there is one side occupied by different pieces.
    state_big_1 = State(
        to_play = Player.ORANGE,
        pieces=[
            (0, 0, Piece.ORANGE_MEDIUM),
            (1, 0, Piece.ORANGE_SMALL),
            (2, 0, Piece.ORANGE_BIG),
        ]
    )
    state_big_2 = State(
        to_play = Player.ORANGE,
        pieces=[
            (0, 0, Piece.ORANGE_MEDIUM),
            (0, 1, Piece.ORANGE_SMALL),
            (0, 2, Piece.ORANGE_BIG),
        ]
    )
    state_big_3 = State(
        to_play = Player.ORANGE,
        pieces=[
            (0, 2, Piece.ORANGE_MEDIUM),
            (1, 2, Piece.ORANGE_SMALL),
            (2, 2, Piece.ORANGE_BIG),
        ]
    )
    state_big_4 = State(
        to_play = Player.ORANGE,
        pieces=[
            (2, 0, Piece.ORANGE_MEDIUM),
            (2, 1, Piece.ORANGE_SMALL),
            (2, 2, Piece.ORANGE_BIG),
        ]
    )
    state_big_5 = State(
        to_play = Player.ORANGE,
        pieces=[
            (2, 0, Piece.ORANGE_MEDIUM),
            (1, 0, Piece.ORANGE_SMALL),
            (0, 0, Piece.ORANGE_BIG),
        ]
    )
    state_big_6 = State(
        to_play = Player.ORANGE,
        pieces=[
            (0, 2, Piece.ORANGE_MEDIUM),
            (0, 1, Piece.ORANGE_SMALL),
            (0, 0, Piece.ORANGE_BIG),
        ]
    )
    state_big_7 = State(
        to_play = Player.ORANGE,
        pieces=[
            (2, 2, Piece.ORANGE_MEDIUM),
            (1, 2, Piece.ORANGE_SMALL),
            (0, 2, Piece.ORANGE_BIG),
        ]
    )
    state_big_8 = State(
        to_play = Player.ORANGE,
        pieces=[
            (2, 2, Piece.ORANGE_MEDIUM),
            (2, 1, Piece.ORANGE_SMALL),
            (2, 0, Piece.ORANGE_BIG),
        ]
    )

    assert state_big_1 == state_big_2
    assert state_big_1 == state_big_3
    assert state_big_1 == state_big_4
    assert state_big_1 == state_big_5
    assert state_big_1 == state_big_6
    assert state_big_1 == state_big_7
    assert state_big_1 == state_big_8

    state_big_a = State(
        to_play = Player.ORANGE,
        pieces=[
            (0, 2, Piece.ORANGE_MEDIUM),
            (1, 0, Piece.ORANGE_SMALL),
            (2, 2, Piece.ORANGE_BIG),
        ]
    )
    state_big_b = State(
        to_play = Player.ORANGE,
        pieces=[
            (0, 0, Piece.ORANGE_MEDIUM),
            (1, 2, Piece.ORANGE_SMALL),
            (2, 2, Piece.ORANGE_BIG),
        ]
    )
    state_big_c = State(
        to_play = Player.ORANGE,
        pieces=[
            (0, 0, Piece.ORANGE_SMALL),
            (0, 1, Piece.ORANGE_MEDIUM),
            (0, 2, Piece.ORANGE_BIG),
        ]
    )
    state_big_d = State(
        to_play = Player.ORANGE,
        pieces=[
            (0, 0, Piece.ORANGE_SMALL),
            (0, 1, Piece.ORANGE_BIG),
            (0, 2, Piece.ORANGE_MEDIUM),
        ]
    )

    assert state_big_1 != state_big_a
    assert state_big_1 != state_big_b
    assert state_big_1 != state_big_c
    assert state_big_1 != state_big_d

    # Test when there is a piece in the middle
    state_1 = State(Player.ORANGE, pieces=[(1, 1, Piece.ORANGE_MEDIUM)])
    state_2 = State(Player.ORANGE, pieces=[(1, 1, Piece.ORANGE_MEDIUM)])
    state_3 = State(Player.ORANGE, pieces=[(1, 1, Piece.ORANGE_BIG)])

    assert state_1 == state_2
    assert state_1 != state_3
    assert state_2 != state_3

    state_1 = State(Player.ORANGE, pieces=[(1, 1, Piece.ORANGE_MEDIUM), (2, 2, Piece.BLUE_MEDIUM)])
    state_2 = State(Player.ORANGE, pieces=[(1, 1, Piece.ORANGE_MEDIUM), (0, 0, Piece.BLUE_MEDIUM)])
    state_3 = State(Player.ORANGE, pieces=[(1, 1, Piece.ORANGE_MEDIUM), (2, 2, Piece.BLUE_BIG)])

    assert state_1 == state_2
    assert state_1 != state_3
    assert state_2 != state_3

    # Test where all cells are filled in
    state_1 = State(
        to_play = Player.ORANGE,
        pieces=[
            (0, 0, Piece.ORANGE_SMALL),
            (0, 1, Piece.ORANGE_MEDIUM),
            (0, 2, Piece.ORANGE_BIG),
            (1, 0, Piece.ORANGE_SMALL),
            (1, 1, Piece.ORANGE_MEDIUM),
            (1, 2, Piece.ORANGE_BIG),
            (2, 0, Piece.BLUE_SMALL),
            (2, 1, Piece.BLUE_MEDIUM),
            (2, 2, Piece.BLUE_BIG),
        ]
    )
    state_2 = State(
        to_play = Player.ORANGE,
        pieces=[
            (2, 0, Piece.ORANGE_SMALL),
            (1, 0, Piece.ORANGE_MEDIUM),
            (0, 0, Piece.ORANGE_BIG),
            (2, 1, Piece.ORANGE_SMALL),
            (1, 1, Piece.ORANGE_MEDIUM),
            (0, 1, Piece.ORANGE_BIG),
            (2, 2, Piece.BLUE_SMALL),
            (1, 2, Piece.BLUE_MEDIUM),
            (0, 2, Piece.BLUE_BIG),
        ]
    )

    assert state_1 == state_2


def test_play_new_piece():
    """Test creating a new state by playing a piece in an existing state.
    Here we test playing a piece that isn't on the board."""

    # TODO: Finish this
    pass

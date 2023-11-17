import unittest
from domain.move import Move
from domain.chess_board import ChessBoard
from domain.teams import TeamEnum
from exception.illegal_move_exception import IllegalMoveException
from logic.move_validations import validate_castle, is_in_check, validate_en_passant, validate_pawn_promotion

"""""""""""""""""""""""
UPPERCASE: whites
lowercase: blacks
 8   r n b q k b n r
 7   p p p p p p p p
 6   . . . . . . . .
 5   . . . . . . . .
 4   . . . . . . . .
 3   . . . . . . . .
 2   P P P P P P P P
 1   R N B Q K B N R

     A B C D E F G H
"""""""""""""""""""""""


class TestCheckValidator(unittest.TestCase):

    def test_is_in_check_diagonally_blacks(self):
        chess_board = ChessBoard()
        chess_board._set_cell('a', 7, 'k')
        chess_board._set_cell('c', 5, 'Q')
        self.assertTrue(is_in_check(
            tuple(['a', 7]),
            TeamEnum.BLACKS.value,
            chess_board
        ))

    def test_is_in_check_diagonally_whites(self):
        chess_board = ChessBoard()
        chess_board._set_cell('d', 3, 'K')
        chess_board._set_cell('g', 6, 'b')
        self.assertTrue(is_in_check(
            tuple(['d', 3]),
            TeamEnum.WHITES.value,
            chess_board
        ))

    def test_is_in_check_orthogonally_whites(self):
        chess_board = ChessBoard()
        chess_board._set_cell('h', 3, 'K')
        chess_board._set_cell('b', 3, 'r')
        chess_board._set_cell('g', 1, '.')
        self.assertTrue(is_in_check(
            tuple(['h', 3]),
            TeamEnum.WHITES.value,
            chess_board
        ))

    def test_is_in_check_orthogonally_blacks(self):
        chess_board = ChessBoard()
        chess_board._set_cell('b', 6, 'k')
        chess_board._set_cell('b', 4, 'Q')
        self.assertTrue(is_in_check(
            tuple(['b', 6]),
            TeamEnum.BLACKS.value,
            chess_board
        ))

    def test_is_in_check_pawn_blacks(self):
        chess_board = ChessBoard()
        chess_board._set_cell('f', 3, 'k')
        chess_board._set_cell('g', 1, '.')
        self.assertTrue(is_in_check(
            tuple(['f', 3]),
            TeamEnum.BLACKS.value,
            chess_board
        ))

    def test_is_in_check_pawn_whites(self):
        chess_board = ChessBoard()
        chess_board._set_cell('d', 6, 'K')
        self.assertTrue(is_in_check(
            tuple(['d', 6]),
            TeamEnum.WHITES.value,
            chess_board
        ))

    def test_is_in_check_knight_whites(self):
        chess_board = ChessBoard()
        chess_board._set_cell('e', 4, 'K')
        chess_board._set_cell('f', 6, 'n')
        self.assertTrue(is_in_check(
            tuple(['e', 4]),
            TeamEnum.WHITES.value,
            chess_board
        ))

    def test_is_in_check_knight_blacks(self):
        chess_board = ChessBoard()
        chess_board._set_cell('d', 4, 'k')
        chess_board._set_cell('b', 5, 'N')
        self.assertTrue(is_in_check(
            tuple(['d', 4]),
            TeamEnum.BLACKS.value,
            chess_board
        ))

    def test_is_not_in_check_piece_in_way_same_team_orthogonal(self):
        chess_board = ChessBoard()
        chess_board._set_cell('e', 4, 'q')
        self.assertFalse(is_in_check(
            tuple(['e', 1]),
            TeamEnum.WHITES.value,
            chess_board
        ))

    def test_is_not_in_check_piece_in_way_other_team_orthogonal(self):
        chess_board = ChessBoard()
        chess_board._set_cell('e', 4, 'R')
        chess_board._set_cell('c', 4, 'B')
        chess_board._set_cell('a', 4, 'k')
        self.assertFalse(is_in_check(
            tuple(['a', 4]),
            TeamEnum.BLACKS.value,
            chess_board
        ))

    def test_is_not_in_check_piece_in_way_same_team_diagonal(self):
        chess_board = ChessBoard()
        chess_board._set_cell('b', 5, 'B')
        self.assertFalse(is_in_check(
            tuple(['e', 8]),
            TeamEnum.BLACKS.value,
            chess_board
        ))

    def test_is_not_in_check_piece_in_way_other_team_diagonal(self):
        chess_board = ChessBoard()
        chess_board._set_cell('b', 3, 'K')
        chess_board._set_cell('e', 6, 'q')
        chess_board._set_cell('c', 4, 'r')
        self.assertFalse(is_in_check(
            tuple(['b', 3]),
            TeamEnum.WHITES.value,
            chess_board
        ))

    def test_is_not_in_check_no_pieces(self):
        chess_board = ChessBoard()
        chess_board._set_cell('f', 4, 'K')
        self.assertFalse(is_in_check(
            tuple(['f', 4]),
            TeamEnum.WHITES.value,
            chess_board
        ))


class TestCastleValidate(unittest.TestCase):

    def test_can_move_whites_left(self):
        chess_board = ChessBoard()
        chess_board._set_cell('b', 1, '.')
        chess_board._set_cell('c', 1, '.')
        chess_board._set_cell('d', 1, '.')
        move = Move(TeamEnum.WHITES.value, 'e1', 'a1', None)

        validate_castle(move, chess_board, [])

        self.assertTrue(True)

    def test_can_move_blacks_right(self):
        chess_board = ChessBoard()
        chess_board._set_cell('f', 8, '.')
        chess_board._set_cell('g', 8, '.')
        move = Move(TeamEnum.BLACKS.value, 'e8', 'h8', None)

        validate_castle(move, chess_board, [])

        self.assertTrue(True)

    def test_cannot_move_passes_check(self):
        chess_board = ChessBoard()
        chess_board._set_cell('b', 8, '.')
        chess_board._set_cell('c', 8, '.')
        chess_board._set_cell('d', 8, '.')
        chess_board._set_cell('b', 7, '.')
        chess_board._set_cell('c', 7, '.')
        chess_board._set_cell('d', 7, '.')
        chess_board._set_cell('b', 6, 'B')
        move = Move(TeamEnum.BLACKS.value, 'e8', 'a8', None)

        with self.assertRaises(IllegalMoveException):
            validate_castle(move, chess_board, [])

    def test_cannot_move_in_check(self):
        chess_board = ChessBoard()
        chess_board._set_cell('b', 8, '.')
        chess_board._set_cell('c', 8, '.')
        chess_board._set_cell('d', 8, '.')
        chess_board._set_cell('b', 7, '.')
        chess_board._set_cell('c', 7, '.')
        chess_board._set_cell('d', 7, '.')
        chess_board._set_cell('b', 5, 'B')
        move = Move(TeamEnum.BLACKS.value, 'e8', 'a8', None)

        with self.assertRaises(IllegalMoveException):
            validate_castle(move, chess_board, [])

    def test_cannot_move_pieces_in_way(self):
        chess_board = ChessBoard()
        move = Move(TeamEnum.WHITES.value, 'e1', 'h1', None)

        with self.assertRaises(IllegalMoveException):
            validate_castle(move, chess_board, [])

    def test_cannot_move_king_moved(self):
        chess_board = ChessBoard()
        chess_board._set_cell('f', 8, '.')
        chess_board._set_cell('g', 8, '.')

        move_history = []
        move_history.append(Move(TeamEnum.BLACKS.value, 'e8', 'f8', None))
        move_history.append(Move(TeamEnum.WHITES.value, 'a1', 'a3', None))
        move_history.append(Move(TeamEnum.BLACKS.value, 'f8', 'e8', None))

        move = Move(TeamEnum.BLACKS.value, 'e8', 'h8', None)
        with self.assertRaises(IllegalMoveException):
            validate_castle(move, chess_board, move_history)

    def test_cannot_move_rook_moved(self):
        chess_board = ChessBoard()
        chess_board._set_cell('b', 1, '.')
        chess_board._set_cell('c', 1, '.')
        chess_board._set_cell('d', 1, '.')

        move_history = []
        move_history.append(Move(TeamEnum.BLACKS.value, 'a1', 'b1', None))
        move_history.append(Move(TeamEnum.WHITES.value, 'g8', 'h6', None))
        move_history.append(Move(TeamEnum.BLACKS.value, 'b1', 'a1', None))

        move = Move(TeamEnum.WHITES.value, 'e1', 'a1', None)
        with self.assertRaises(IllegalMoveException):
            validate_castle(move, chess_board, move_history)


class TestEnPassantValidate(unittest.TestCase):

    def test_captured_pawn_didnt_move_in_previous_move(self):
        chess_board = ChessBoard()

        chess_board._set_cell('e', 5, 'p')
        chess_board._set_cell('f', 5, 'P')
        move = Move(TeamEnum.WHITES.value, 'f5', 'e6', None)

        move_history = []
        move_history.append(Move(TeamEnum.WHITES.value, 'f4', 'f5', None))
        move_history.append(Move(TeamEnum.BLACKS.value, 'e7', 'e5', None))
        move_history.append(Move(TeamEnum.WHITES.value, 'h2', 'h3', None))
        move_history.append(Move(TeamEnum.BLACKS.value, 'h7', 'h6', None))

        with self.assertRaises(IllegalMoveException):
            validate_en_passant(move, chess_board, move_history)


    def test_wrong_rank(self):
        chess_board = ChessBoard()

        chess_board._set_cell('e', 4, 'p')
        chess_board._set_cell('f', 4, 'P')

        move = Move(TeamEnum.WHITES.value, 'f4', 'e5', None)

        move_history = []
        move_history.append(Move(TeamEnum.BLACKS.value, 'e7', 'e5', None))
        move_history.append(Move(TeamEnum.WHITES.value, 'f2', 'f4', None))
        move_history.append(Move(TeamEnum.BLACKS.value, 'e5', 'e4', None))

        with self.assertRaises(IllegalMoveException):
            validate_en_passant(move, chess_board, move_history)

    def test_cannot_capture_pawn_moved_one_square(self):
        chess_board = ChessBoard()

        chess_board._set_cell('e', 5, 'p')
        chess_board._set_cell('f', 5, 'P')
        move = Move(TeamEnum.WHITES.value, 'f5', 'e6', None)

        move_history = []
        move_history.append(Move(TeamEnum.BLACKS.value, 'e7', 'e6', None))
        move_history.append(Move(TeamEnum.WHITES.value, 'h2', 'h3', None))#pass move
        move_history.append(Move(TeamEnum.BLACKS.value, 'e6', 'e5', None))

        with self.assertRaises(IllegalMoveException):
            validate_en_passant(move, chess_board, move_history)


    def test_cannot_move_into_check(self):
        chess_board = ChessBoard()

        chess_board._set_cell('e', 5, 'p')
        chess_board._set_cell('f', 5, 'P')
        chess_board._set_cell('g', 6, 'b')
        chess_board._set_cell('d', 3, 'K')
        chess_board._set_cell('e', 1, '.')
        move = Move(TeamEnum.WHITES.value, 'f5', 'e6', None)

        move_history = []
        move_history.append(Move(TeamEnum.BLACKS.value, 'e7', 'e5', None))

        with self.assertRaises(IllegalMoveException):
            validate_en_passant(move, chess_board, move_history)

    def test_correct_en_passant_white(self):
        chess_board = ChessBoard()
        chess_board._set_cell('e', 5, 'p')
        chess_board._set_cell('f', 5, 'P')
        move = Move(TeamEnum.WHITES.value, 'f5', 'e6', None)

        move_history = []
        move_history.append(Move(TeamEnum.BLACKS.value, 'e7', 'e5', None))

        try:
            validate_en_passant(move, chess_board, move_history)
        except IllegalMoveException as exception:
            self.fail(f"validate_en_passant raised {type(exception).__name__}")

    def test_correct_en_passant_black(self):
        chess_board = ChessBoard()
        chess_board._set_cell('e', 4, 'p')
        chess_board._set_cell('f', 4, 'P')
        move = Move(TeamEnum.BLACKS.value, 'e4', 'f3', None)

        move_history = []
        move_history.append(Move(TeamEnum.WHITES.value, 'f2', 'f4', None))

        try:
            validate_en_passant(move, chess_board, move_history)
        except IllegalMoveException as exception:
            self.fail(f"validate_en_passant raised {type(exception).__name__}")
               
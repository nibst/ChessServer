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
        move = Move('WHITES', 'e1', 'a1', None)

        validate_castle(move, chess_board, [])

        self.assertTrue(True)

    def test_can_move_blacks_right(self):
        chess_board = ChessBoard()
        chess_board._set_cell('f', 8, '.')
        chess_board._set_cell('g', 8, '.')
        move = Move('BLACKS', 'e8', 'h8', None)

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
        move = Move('BLACKS', 'e8', 'a8', None)

        self.assertRaises(
            IllegalMoveException,
            validate_castle,
            move,
            chess_board,
            []
        )

    def test_cannot_move_in_check(self):
        chess_board = ChessBoard()
        chess_board._set_cell('b', 8, '.')
        chess_board._set_cell('c', 8, '.')
        chess_board._set_cell('d', 8, '.')
        chess_board._set_cell('b', 7, '.')
        chess_board._set_cell('c', 7, '.')
        chess_board._set_cell('d', 7, '.')
        chess_board._set_cell('b', 5, 'B')
        move = Move('BLACKS', 'e8', 'a8', None)

        self.assertRaises(
            IllegalMoveException,
            validate_castle,
            move,
            chess_board,
            []
        )

    def test_cannot_move_pieces_in_way(self):
        chess_board = ChessBoard()
        move = Move('WHITES', 'e1', 'h1', None)

        self.assertRaises(
            IllegalMoveException,
            validate_castle,
            move,
            chess_board,
            []
        )

    def test_cannot_move_king_moved(self):
        chess_board = ChessBoard()
        chess_board._set_cell('f', 8, '.')
        chess_board._set_cell('g', 8, '.')

        move_history = []
        move_history.append(Move('BLACKS', 'e8', 'f8', None))
        move_history.append(Move('WHITES', 'a1', 'a3', None))
        move_history.append(Move('BLACKS', 'f8', 'e8', None))

        move = Move('BLACKS', 'e8', 'h8', None)
        self.assertRaises(
            IllegalMoveException,
            validate_castle,
            move,
            chess_board,
            move_history
        )

    def test_cannot_move_rook_moved(self):
        chess_board = ChessBoard()
        chess_board._set_cell('b', 1, '.')
        chess_board._set_cell('c', 1, '.')
        chess_board._set_cell('d', 1, '.')

        move_history = []
        move_history.append(Move('BLACKS', 'a1', 'b1', None))
        move_history.append(Move('WHITES', 'g8', 'h6', None))
        move_history.append(Move('BLACKS', 'b1', 'a1', None))

        move = Move('WHITES', 'e1', 'a1', None)
        self.assertRaises(
            IllegalMoveException,
            validate_castle,
            move,
            chess_board,
            move_history
        )

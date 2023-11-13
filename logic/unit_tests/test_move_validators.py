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
        chess_board._set_cell(7, 'a', 'k')
        chess_board._set_cell(5, 'c', 'Q')
        self.assertTrue(is_in_check(
            tuple([7, 'a']),
            TeamEnum.BLACKS.value,
            chess_board
        ))

    def test_is_in_check_diagonally_whites(self):
        chess_board = ChessBoard()
        chess_board._set_cell(3, 'd', 'K')
        chess_board._set_cell(6, 'g', 'b')
        self.assertTrue(is_in_check(
            tuple([3, 'd']),
            TeamEnum.WHITES.value,
            chess_board
        ))

    def test_is_in_check_orthogonally_whites(self):
        chess_board = ChessBoard()
        chess_board._set_cell(3, 'h', 'K')
        chess_board._set_cell(3, 'b', 'r')
        chess_board._set_cell(1, 'g', '.')
        self.assertTrue(is_in_check(
            tuple([3, 'h']),
            TeamEnum.WHITES.value,
            chess_board
        ))

    def test_is_in_check_orthogonally_blacks(self):
        chess_board = ChessBoard()
        chess_board._set_cell(6, 'b', 'k')
        chess_board._set_cell(4, 'b', 'Q')
        self.assertTrue(is_in_check(
            tuple([6, 'b']),
            TeamEnum.BLACKS.value,
            chess_board
        ))

    def test_is_in_check_pawn_blacks(self):
        chess_board = ChessBoard()
        chess_board._set_cell(3, 'f', 'k')
        chess_board._set_cell(1, 'g', '.')
        self.assertTrue(is_in_check(
            tuple([3, 'f']),
            TeamEnum.BLACKS.value,
            chess_board
        ))

    def test_is_in_check_pawn_whites(self):
        chess_board = ChessBoard()
        chess_board._set_cell(6, 'd', 'K')
        self.assertTrue(is_in_check(
            tuple([6, 'd']),
            TeamEnum.WHITES.value,
            chess_board
        ))

    def test_is_in_check_knight_whites(self):
        chess_board = ChessBoard()
        chess_board._set_cell(4, 'e', 'K')
        chess_board._set_cell(6, 'f', 'n')
        self.assertTrue(is_in_check(
            tuple([4, 'e']),
            TeamEnum.WHITES.value,
            chess_board
        ))

    def test_is_in_check_knight_blacks(self):
        chess_board = ChessBoard()
        chess_board._set_cell(4, 'd', 'k')
        chess_board._set_cell(5, 'b', 'N')
        self.assertTrue(is_in_check(
            tuple([4, 'd']),
            TeamEnum.BLACKS.value,
            chess_board
        ))

    def test_is_not_in_check_piece_in_way_same_team_orthogonal(self):
        chess_board = ChessBoard()
        chess_board._set_cell(4, 'e', 'q')
        self.assertFalse(is_in_check(
            tuple([1, 'e']),
            TeamEnum.WHITES.value,
            chess_board
        ))

    def test_is_not_in_check_piece_in_way_other_team_orthogonal(self):
        chess_board = ChessBoard()
        chess_board._set_cell(4, 'e', 'R')
        chess_board._set_cell(4, 'c', 'B')
        chess_board._set_cell(4, 'a', 'k')
        self.assertFalse(is_in_check(
            tuple([4, 'a']),
            TeamEnum.BLACKS.value,
            chess_board
        ))

    def test_is_not_in_check_piece_in_way_same_team_diagonal(self):
        chess_board = ChessBoard()
        chess_board._set_cell(5, 'b', 'B')
        self.assertFalse(is_in_check(
            tuple([8, 'e']),
            TeamEnum.BLACKS.value,
            chess_board
        ))

    def test_is_not_in_check_piece_in_way_other_team_diagonal(self):
        chess_board = ChessBoard()
        chess_board._set_cell(3, 'b', 'K')
        chess_board._set_cell(6, 'e', 'q')
        chess_board._set_cell(4, 'c', 'r')
        self.assertFalse(is_in_check(
            tuple([3, 'b']),
            TeamEnum.WHITES.value,
            chess_board
        ))

    def test_is_not_in_check_no_pieces(self):
        chess_board = ChessBoard()
        chess_board._set_cell(4, 'f', 'K')
        self.assertFalse(is_in_check(
            tuple([4, 'f']),
            TeamEnum.WHITES.value,
            chess_board
        ))


class TestCastleValidate(unittest.TestCase):

    def test_can_move_whites_left(self):
        chess_board = ChessBoard()
        chess_board._set_cell(1, 'b', '.')
        chess_board._set_cell(1, 'c', '.')
        chess_board._set_cell(1, 'd', '.')
        move = Move('WHITES', '1e', '1a', None)

        validate_castle(move, chess_board, [])

        self.assertTrue(True)

    def test_can_move_blacks_right(self):
        chess_board = ChessBoard()
        chess_board._set_cell(8, 'f', '.')
        chess_board._set_cell(8, 'g', '.')
        move = Move('BLACKS', '8e', '8h', None)

        validate_castle(move, chess_board, [])

        self.assertTrue(True)

    def test_cannot_move_passes_check(self):
        chess_board = ChessBoard()
        chess_board._set_cell(8, 'b', '.')
        chess_board._set_cell(8, 'c', '.')
        chess_board._set_cell(8, 'd', '.')
        chess_board._set_cell(7, 'b', '.')
        chess_board._set_cell(7, 'c', '.')
        chess_board._set_cell(7, 'd', '.')
        chess_board._set_cell(6, 'b', 'B')
        move = Move('BLACKS', '8e', '8a', None)

        self.assertRaises(
            IllegalMoveException,
            validate_castle,
            move,
            chess_board,
            []
        )

    def test_cannot_move_in_check(self):
        chess_board = ChessBoard()
        chess_board._set_cell(8, 'b', '.')
        chess_board._set_cell(8, 'c', '.')
        chess_board._set_cell(8, 'd', '.')
        chess_board._set_cell(7, 'b', '.')
        chess_board._set_cell(7, 'c', '.')
        chess_board._set_cell(7, 'd', '.')
        chess_board._set_cell(5, 'b', 'B')
        move = Move('BLACKS', '8e', '8a', None)

        self.assertRaises(
            IllegalMoveException,
            validate_castle,
            move,
            chess_board,
            []
        )

    def test_cannot_move_pieces_in_way(self):
        chess_board = ChessBoard()
        move = Move('WHITES', '1e', '1h', None)

        self.assertRaises(
            IllegalMoveException,
            validate_castle,
            move,
            chess_board,
            []
        )

    def test_cannot_move_king_moved(self):
        chess_board = ChessBoard()
        chess_board._set_cell(8, 'f', '.')
        chess_board._set_cell(8, 'g', '.')

        move_history = []
        move_history.append(Move('BLACKS', '8e', '8f', None))
        move_history.append(Move('WHITES', '1a', '3a', None))
        move_history.append(Move('BLACKS', '8f', '8e', None))

        move = Move('BLACKS', '8e', '8h', None)
        self.assertRaises(
            IllegalMoveException,
            validate_castle,
            move,
            chess_board,
            move_history
        )

    def test_cannot_move_rook_moved(self):
        chess_board = ChessBoard()
        chess_board._set_cell(1, 'b', '.')
        chess_board._set_cell(1, 'c', '.')
        chess_board._set_cell(1, 'd', '.')

        move_history = []
        move_history.append(Move('BLACKS', '1a', '1b', None))
        move_history.append(Move('WHITES', '8g', '6h', None))
        move_history.append(Move('BLACKS', '1b', '1a', None))

        move = Move('WHITES', '1e', '1a', None)
        self.assertRaises(
            IllegalMoveException,
            validate_castle,
            move,
            chess_board,
            move_history
        )

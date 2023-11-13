import unittest
from domain.move import Move
from domain.chess_board import ChessBoard
from logic.move_identifiers import is_castle, is_en_passant, is_pawn_promotion

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


class TestEnPassantIdentify(unittest.TestCase):

    def test_is_move_whites_left(self):
        chess_board = ChessBoard()
        chess_board._set_cell(5, 'e', 'p')
        chess_board._set_cell(5, 'f', 'P')
        move = Move('WHITES', '5f', '6e', None)
        self.assertTrue(is_en_passant(move, chess_board))

    def test_is_move_whites_right(self):
        chess_board = ChessBoard()
        chess_board._set_cell(5, 'h', 'p')
        chess_board._set_cell(5, 'g', 'P')
        move = Move('WHITES', '5g', '6h', None)
        self.assertTrue(is_en_passant(move, chess_board))

    def test_is_move_blacks_left(self):
        chess_board = ChessBoard()
        chess_board._set_cell(4, 'e', 'p')
        chess_board._set_cell(4, 'd', 'P')
        move = Move('BLACKS', '4e', '3d', None)
        self.assertTrue(is_en_passant(move, chess_board))

    def test_is_move_blacks_right(self):
        chess_board = ChessBoard()
        chess_board._set_cell(4, 'a', 'p')
        chess_board._set_cell(4, 'b', 'P')
        move = Move('BLACKS', '4a', '3b', None)
        self.assertTrue(is_en_passant(move, chess_board))

    def test_is_not_move_another_piece_player(self):
        chess_board = ChessBoard()
        chess_board._set_cell(5, 'h', 'p')
        chess_board._set_cell(5, 'g', 'K')
        move = Move('WHITES', '5g', '6h', None)
        self.assertFalse(is_en_passant(move, chess_board))

    def test_is_not_move_another_piece_opponent(self):
        chess_board = ChessBoard()
        chess_board._set_cell(4, 'e', 'p')
        chess_board._set_cell(4, 'd', 'K')
        move = Move('BLACKS', '4e', '3d', None)
        self.assertFalse(is_en_passant(move, chess_board))

    def test_is_not_move_piece_in_way(self):
        chess_board = ChessBoard()
        chess_board._set_cell(5, 'h', 'p')
        chess_board._set_cell(6, 'h', 'n')
        chess_board._set_cell(5, 'g', 'P')
        move = Move('WHITES', '5g', '6h', None)
        self.assertFalse(is_en_passant(move, chess_board))


class TestCastleIdentify(unittest.TestCase):

    def test_is_move_whites_left(self):
        chess_board = ChessBoard()
        move = Move('WHITES', '1e', '1a', None)
        self.assertTrue(is_castle(move, chess_board))

    def test_is_move_whites_right(self):
        chess_board = ChessBoard()
        move = Move('WHITES', '1e', '1h', None)
        self.assertTrue(is_castle(move, chess_board))

    def test_is_move_blacks_left(self):
        chess_board = ChessBoard()
        move = Move('BLACKS', '8e', '8a', None)
        self.assertTrue(is_castle(move, chess_board))

    def test_is_move_blacks_right(self):
        chess_board = ChessBoard()
        move = Move('BLACKS', '8e', '8h', None)
        self.assertTrue(is_castle(move, chess_board))

    def test_is_not_move_wrong_start_piece(self):
        chess_board = ChessBoard()
        chess_board._set_cell(8, 'e', 'q')
        move = Move('BLACKS', '8e', '8h', None)
        self.assertFalse(is_castle(move, chess_board))

    def test_is_not_move_wrong_start_position(self):
        chess_board = ChessBoard()
        chess_board._set_cell(7, 'e', 'k')
        move = Move('BLACKS', '7e', '8a', None)
        self.assertFalse(is_castle(move, chess_board))

    def test_is_not_move_wrong_end_piece(self):
        chess_board = ChessBoard()
        chess_board._set_cell(8, 'h', 'p')
        move = Move('BLACKS', '8e', '8h', None)
        self.assertFalse(is_castle(move, chess_board))

    def test_is_not_move_wrong_end_position(self):
        chess_board = ChessBoard()
        chess_board._set_cell(7, 'h', 'r')
        move = Move('BLACKS', '8e', '7h', None)
        self.assertFalse(is_castle(move, chess_board))


class TestPawnPromotionIdentify(unittest.TestCase):

    def test_is_move_whites(self):
        chess_board = ChessBoard()
        chess_board._set_cell(7, 'g', 'P')
        chess_board._set_cell(8, 'g', '.')
        move = Move('WHITES', '7g', '8g', 'Q')
        self.assertTrue(is_pawn_promotion(move, chess_board))

    def test_is_move_blacks(self):
        chess_board = ChessBoard()
        chess_board._set_cell(2, 'd', 'p')
        chess_board._set_cell(1, 'd', '.')
        move = Move('BLACKS', '2d', '1d', None)
        self.assertTrue(is_pawn_promotion(move, chess_board))

    def test_is_move_eating(self):
        chess_board = ChessBoard()
        chess_board._set_cell(2, 'd', 'p')
        chess_board._set_cell(1, 'c', 'Q')
        move = Move('BLACKS', '2d', '1c', None)
        self.assertTrue(is_pawn_promotion(move, chess_board))

    def test_is_not_move_wrong_rank(self):
        chess_board = ChessBoard()
        chess_board._set_cell(6, 'g', 'P')
        chess_board._set_cell(7, 'g', '.')
        move = Move('WHITES', '6g', '7g', 'Q')
        self.assertFalse(is_pawn_promotion(move, chess_board))

    def test_is_not_move_wrong_piece(self):
        chess_board = ChessBoard()
        chess_board._set_cell(2, 'd', 'k')
        chess_board._set_cell(1, 'c', 'Q')
        move = Move('BLACKS', '2d', '1c', None)
        self.assertFalse(is_pawn_promotion(move, chess_board))

    def test_is_not_move_blocked(self):
        chess_board = ChessBoard()
        chess_board._set_cell(7, 'g', 'P')
        chess_board._set_cell(8, 'g', 'k')
        move = Move('WHITES', '7g', '8g', 'Q')
        self.assertFalse(is_pawn_promotion(move, chess_board))

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
        chess_board._set_cell('e', 5, 'p')
        chess_board._set_cell('f', 5, 'P')
        move = Move('WHITES', 'f5', 'e6', None)
        self.assertTrue(is_en_passant(move, chess_board))

    def test_is_move_whites_right(self):
        chess_board = ChessBoard()
        chess_board._set_cell('h', 5, 'p')
        chess_board._set_cell('g', 5, 'P')
        move = Move('WHITES', 'g5', 'h6', None)
        self.assertTrue(is_en_passant(move, chess_board))

    def test_is_move_blacks_left(self):
        chess_board = ChessBoard()
        chess_board._set_cell('e', 4, 'p')
        chess_board._set_cell('d', 4, 'P')
        move = Move('BLACKS', 'e4', 'd3', None)
        self.assertTrue(is_en_passant(move, chess_board))

    def test_is_move_blacks_right(self):
        chess_board = ChessBoard()
        chess_board._set_cell('a', 4, 'p')
        chess_board._set_cell('b', 4, 'P')
        move = Move('BLACKS', 'a4', 'b3', None)
        self.assertTrue(is_en_passant(move, chess_board))

    def test_is_not_move_another_piece_player(self):
        chess_board = ChessBoard()
        chess_board._set_cell('h', 5, 'p')
        chess_board._set_cell('g', 5, 'K')
        move = Move('WHITES', 'g5', 'h6', None)
        self.assertFalse(is_en_passant(move, chess_board))

    def test_is_not_move_another_piece_opponent(self):
        chess_board = ChessBoard()
        chess_board._set_cell('e', 4, 'p')
        chess_board._set_cell('d', 4, 'K')
        move = Move('BLACKS', 'e4', 'd3', None)
        self.assertFalse(is_en_passant(move, chess_board))

    def test_is_not_move_piece_in_way(self):
        chess_board = ChessBoard()
        chess_board._set_cell('h', 5, 'p')
        chess_board._set_cell('h', 6, 'n')
        chess_board._set_cell('g', 5, 'P')
        move = Move('WHITES', 'g5', 'h6', None)
        self.assertFalse(is_en_passant(move, chess_board))


class TestCastleIdentify(unittest.TestCase):

    def test_is_move_whites_left(self):
        chess_board = ChessBoard()
        move = Move('WHITES', 'e1', 'a1', None)
        self.assertTrue(is_castle(move, chess_board))

    def test_is_move_whites_right(self):
        chess_board = ChessBoard()
        move = Move('WHITES', 'e1', 'h1', None)
        self.assertTrue(is_castle(move, chess_board))

    def test_is_move_blacks_left(self):
        chess_board = ChessBoard()
        move = Move('BLACKS', 'e8', 'a8', None)
        self.assertTrue(is_castle(move, chess_board))

    def test_is_move_blacks_right(self):
        chess_board = ChessBoard()
        move = Move('BLACKS', 'e8', 'h8', None)
        self.assertTrue(is_castle(move, chess_board))

    def test_is_not_move_wrong_start_piece(self):
        chess_board = ChessBoard()
        chess_board._set_cell('e', 8, 'q')
        move = Move('BLACKS', 'e8', 'h8', None)
        self.assertFalse(is_castle(move, chess_board))

    def test_is_not_move_wrong_start_position(self):
        chess_board = ChessBoard()
        chess_board._set_cell('e', 7, 'k')
        move = Move('BLACKS', 'e7', 'a8', None)
        self.assertFalse(is_castle(move, chess_board))

    def test_is_not_move_wrong_end_piece(self):
        chess_board = ChessBoard()
        chess_board._set_cell('h', 8, 'p')
        move = Move('BLACKS', 'e8', 'h8', None)
        self.assertFalse(is_castle(move, chess_board))

    def test_is_not_move_wrong_end_position(self):
        chess_board = ChessBoard()
        chess_board._set_cell('h', 7, 'r')
        move = Move('BLACKS', 'e8', 'h7', None)
        self.assertFalse(is_castle(move, chess_board))


class TestPawnPromotionIdentify(unittest.TestCase):

    def test_is_move_whites(self):
        chess_board = ChessBoard()
        chess_board._set_cell('g', 7, 'P')
        chess_board._set_cell('g', 8, '.')
        move = Move('WHITES', 'g7', 'g8', 'Q')
        self.assertTrue(is_pawn_promotion(move, chess_board))

    def test_is_move_blacks(self):
        chess_board = ChessBoard()
        chess_board._set_cell('d', 2, 'p')
        chess_board._set_cell('d', 1, '.')
        move = Move('BLACKS', 'd2', 'd1', None)
        self.assertTrue(is_pawn_promotion(move, chess_board))

    def test_is_move_eating(self):
        chess_board = ChessBoard()
        chess_board._set_cell('d', 2, 'p')
        chess_board._set_cell('c', 1, 'Q')
        move = Move('BLACKS', 'd2', 'c1', None)
        self.assertTrue(is_pawn_promotion(move, chess_board))

    def test_is_not_move_wrong_rank(self):
        chess_board = ChessBoard()
        chess_board._set_cell('g', 6, 'P')
        chess_board._set_cell('g', 7, '.')
        move = Move('WHITES', 'g6', 'g7', 'Q')
        self.assertFalse(is_pawn_promotion(move, chess_board))

    def test_is_not_move_wrong_piece(self):
        chess_board = ChessBoard()
        chess_board._set_cell('d', 2, 'k')
        chess_board._set_cell('c', 1, 'Q')
        move = Move('BLACKS', 'd2', 'c1', None)
        self.assertFalse(is_pawn_promotion(move, chess_board))

    def test_is_not_move_blocked(self):
        chess_board = ChessBoard()
        chess_board._set_cell('g', 7, 'P')
        chess_board._set_cell('g', 8, 'k')
        move = Move('WHITES', 'g7', 'g8', 'Q')
        self.assertFalse(is_pawn_promotion(move, chess_board))

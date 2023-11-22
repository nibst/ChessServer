import unittest
from domain.move import Move
from domain.chess_board import ChessBoard
from domain.teams import TeamEnum
from exception.illegal_move_exception import IllegalMoveException
from logic.move_constructors import *   

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


class TestCastleConstructor(unittest.TestCase):

    def test_castle_right_blacks(self):
        chess_board = ChessBoard()
        chess_board._set_cell('f', 8,'.')
        chess_board._set_cell('g', 8, '.')
        castle_move = Move(TeamEnum.BLACKS.value, "e8", "h8", None)
        
        execute_function = create_castle_steps(castle_move)
        execute_function(chess_board)
        self.assertEqual('.', chess_board._get_cell('e', 8))
        self.assertEqual('r', chess_board._get_cell('f', 8))
        self.assertEqual('k', chess_board._get_cell('g', 8))
        self.assertEqual('.', chess_board._get_cell('h', 8))

    def test_castle_left_blacks(self):
        chess_board = ChessBoard()
        chess_board._set_cell('b', 8, '.')
        chess_board._set_cell('c', 8, '.')
        chess_board._set_cell('d', 8, '.')
        castle_move = Move(TeamEnum.BLACKS.value, "e8", "a8", None)

        execute_function = create_castle_steps(castle_move)
        execute_function(chess_board)
        self.assertEqual('.', chess_board._get_cell('a', 8))
        self.assertEqual('.', chess_board._get_cell('b', 8))
        self.assertEqual('k', chess_board._get_cell('c', 8))
        self.assertEqual('r', chess_board._get_cell('d', 8))
        self.assertEqual('.', chess_board._get_cell('e', 8))

    def test_castle_right_whites(self):
        chess_board = ChessBoard()
        chess_board._set_cell('f', 1, '.')
        chess_board._set_cell('g', 1, '.')
        castle_move = Move(TeamEnum.BLACKS.value, "e1", "h1", None)

        execute_function = create_castle_steps(castle_move)
        execute_function(chess_board)
        self.assertEqual('.', chess_board._get_cell('e', 1))
        self.assertEqual('R', chess_board._get_cell('f', 1))
        self.assertEqual('K', chess_board._get_cell('g', 1))
        self.assertEqual('.', chess_board._get_cell('h', 1))

    def test_castle_left_whites(self):
        chess_board = ChessBoard()
        chess_board._set_cell('b', 1, '.')
        chess_board._set_cell('c', 1, '.')
        chess_board._set_cell('d', 1, '.')
        castle_move = Move(TeamEnum.WHITES.value, "e1", "a1", None)

        execute_function = create_castle_steps(castle_move)
        execute_function(chess_board)
        self.assertEqual('.', chess_board._get_cell('a', 1))
        self.assertEqual('.', chess_board._get_cell('b', 1))
        self.assertEqual('K', chess_board._get_cell('c', 1))
        self.assertEqual('R', chess_board._get_cell('d', 1))
        self.assertEqual('.', chess_board._get_cell('e', 1))


class TestEnPassantConstruction(unittest.TestCase):

    def test_en_passant_right_blacks(self):
        chess_board = ChessBoard()
        chess_board._set_cell('f', 4, 'P')
        chess_board._set_cell('e', 4, 'p')
        en_passant_move = Move(TeamEnum.BLACKS.value, "e4", "f3", None)

        execute_function = create_en_passant_steps(en_passant_move)
        execute_function(chess_board)
        self.assertEqual('.', chess_board._get_cell('e', 4))
        self.assertEqual('.', chess_board._get_cell('f', 4))
        self.assertEqual('p', chess_board._get_cell('f', 3))

    def test_en_passant_left_blacks(self):
        chess_board = ChessBoard()
        chess_board._set_cell('d', 4, 'P')
        chess_board._set_cell('e', 4, 'p')
        en_passant_move = Move(TeamEnum.BLACKS.value, "e4", "d3", None)

        execute_function = create_en_passant_steps(en_passant_move)
        execute_function(chess_board)
        self.assertEqual('.', chess_board._get_cell('e', 4))
        self.assertEqual('.', chess_board._get_cell('d', 4))
        self.assertEqual('p', chess_board._get_cell('d', 3))

    def test_en_passant_right_whites(self):
        chess_board = ChessBoard()
        chess_board._set_cell('d', 5, 'P')
        chess_board._set_cell('e', 5, 'p')
        en_passant_move = Move(TeamEnum.WHITES.value, "d5", "e6", None)

        execute_function = create_en_passant_steps(en_passant_move)
        execute_function(chess_board)
        
        self.assertEqual('.', chess_board._get_cell('d', 5))   
        self.assertEqual('.', chess_board._get_cell('e', 5))
        self.assertEqual('P', chess_board._get_cell('e', 6))

    def test_en_passant_left_whites(self):
        chess_board = ChessBoard()
        chess_board._set_cell('d', 5, 'P')
        chess_board._set_cell('c', 5, 'p')
        en_passant_move = Move(TeamEnum.WHITES.value, "d5", "c6", None)

        execute_function = create_en_passant_steps(en_passant_move)
        execute_function(chess_board)
        self.assertEqual('.', chess_board._get_cell('d', 5))
        self.assertEqual('.', chess_board._get_cell('c', 5))   
        self.assertEqual('P', chess_board._get_cell('c', 6))

class TestPawnPromotionConstruction(unittest.TestCase):
    def test_white_promote_going_straight_foward(self):
        chessboard = ChessBoard()
        chessboard._set_cell('b', 7, 'P')
        chessboard._set_cell('b', 8, '.')

        pawn_promotion_move = Move(TeamEnum.WHITES.value, "b7", "b8", 'R')
        execute_function = create_pawn_promotion_steps(pawn_promotion_move)
        execute_function(chessboard)
        self.assertEqual('Q',chessboard._get_cell('b',8))

    def test_black_promote_going_straight_foward(self):
        chessboard = ChessBoard()
        chessboard._set_cell('b', 2, 'p')
        chessboard._set_cell('b', 1, '.')

        pawn_promotion_move = Move(TeamEnum.BLACKS.value, "b2", "b1", 'q')
        execute_function = create_pawn_promotion_steps(pawn_promotion_move)
        execute_function(chessboard)
        self.assertEqual('q',chessboard._get_cell('b',1))


    def test_promote_capture_left(self):
        chessboard = ChessBoard()
        chessboard._set_cell('b', 2, 'p')

        pawn_promotion_move = Move(TeamEnum.BLACKS.value, "b2", "a1", 'q')
        execute_function = create_pawn_promotion_steps(pawn_promotion_move)
        execute_function(chessboard)
        self.assertEqual('q',chessboard._get_cell('a',1))


    def test_promote_capture_right(self):
        chessboard = ChessBoard()
        chessboard._set_cell('b', 7, 'P')

        pawn_promotion_move = Move(TeamEnum.WHITES.value, "b7", "c8", 'Q')
        execute_function = create_pawn_promotion_steps(pawn_promotion_move)
        execute_function(chessboard)
        self.assertEqual('Q',chessboard._get_cell('c',8))

    def test_promote_to_horse(self):
        chessboard = ChessBoard()
        chessboard._set_cell('c', 7, 'P')
        chessboard._set_cell('c', 8, '.')

        pawn_promotion_move = Move(TeamEnum.WHITES.value, "c7", "c8", 'N')
        execute_function = create_pawn_promotion_steps(pawn_promotion_move)
        execute_function(chessboard)
        self.assertEqual('N',chessboard._get_cell('c',8))

    def test_promote_to_queen(self):
        chessboard = ChessBoard()
        chessboard._set_cell('c', 7, 'P')
        chessboard._set_cell('c', 8, '.')

        pawn_promotion_move = Move(TeamEnum.WHITES.value, "c7", "c8", 'Q')
        execute_function = create_pawn_promotion_steps(pawn_promotion_move)
        execute_function(chessboard)  
        self.assertEqual('Q',chessboard._get_cell('c',8))

    def test_promote_to_rook(self):
        chessboard = ChessBoard()
        chessboard._set_cell('c', 2, 'p')
        chessboard._set_cell('c', 1, '.')

        pawn_promotion_move = Move(TeamEnum.BLACKS.value, "c2", "c1", 'r')
        execute_function = create_pawn_promotion_steps(pawn_promotion_move)
        execute_function(chessboard) 
        self.assertEqual('r',chessboard._get_cell('c',1))

    def test_promote_to_bishop(self):
        chessboard = ChessBoard()
        chessboard._set_cell('c', 2, 'p')
        chessboard._set_cell('c', 1, '.')

        pawn_promotion_move = Move(TeamEnum.BLACKS.value, "c2", "c1", 'b')
        execute_function = create_pawn_promotion_steps(pawn_promotion_move)
        execute_function(chessboard) 
        self.assertEqual('b',chessboard._get_cell('c',1))


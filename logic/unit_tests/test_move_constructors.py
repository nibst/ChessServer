import unittest
from domain.move import Move
from domain.chess_board import ChessBoard
from domain.teams import TeamEnum
from exception.illegal_move_exception import IllegalMoveException
from logic.move_constructors import create_castle_steps

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
        chess_board._set_cell(8, 'f', '.')
        chess_board._set_cell(8, 'g', '.')
        castle_move = Move(TeamEnum.BLACKS.value, "8e", "8h", None)

        execute_function = create_castle_steps(castle_move)
        execute_function(chess_board)
        self.assertEquals('.', chess_board._get_cell(8, 'e'))
        self.assertEquals('r', chess_board._get_cell(8, 'f'))
        self.assertEquals('k', chess_board._get_cell(8, 'g'))
        self.assertEquals('.', chess_board._get_cell(8, 'h'))

    def test_castle_left_blacks(self):
        chess_board = ChessBoard()
        chess_board._set_cell(8, 'b', '.')
        chess_board._set_cell(8, 'c', '.')
        chess_board._set_cell(8, 'd', '.')
        castle_move = Move(TeamEnum.BLACKS.value, "8e", "8a", None)

        execute_function = create_castle_steps(castle_move)
        execute_function(chess_board)
        self.assertEquals('.', chess_board._get_cell(8, 'a'))
        self.assertEquals('.', chess_board._get_cell(8, 'b'))
        self.assertEquals('k', chess_board._get_cell(8, 'c'))
        self.assertEquals('r', chess_board._get_cell(8, 'd'))
        self.assertEquals('.', chess_board._get_cell(8, 'e'))

    def test_castle_right_whites(self):
        chess_board = ChessBoard()
        chess_board._set_cell(1, 'f', '.')
        chess_board._set_cell(1, 'g', '.')
        castle_move = Move(TeamEnum.BLACKS.value, "1e", "1h", None)

        execute_function = create_castle_steps(castle_move)
        execute_function(chess_board)
        self.assertEquals('.', chess_board._get_cell(1, 'e'))
        self.assertEquals('R', chess_board._get_cell(1, 'f'))
        self.assertEquals('K', chess_board._get_cell(1, 'g'))
        self.assertEquals('.', chess_board._get_cell(1, 'h'))

    def test_castle_left_whites(self):
        chess_board = ChessBoard()
        chess_board._set_cell(1, 'b', '.')
        chess_board._set_cell(1, 'c', '.')
        chess_board._set_cell(1, 'd', '.')
        castle_move = Move(TeamEnum.WHITES.value, "1e", "1a", None)

        execute_function = create_castle_steps(castle_move)
        execute_function(chess_board)
        self.assertEquals('.', chess_board._get_cell(1, 'a'))
        self.assertEquals('.', chess_board._get_cell(1, 'b'))
        self.assertEquals('K', chess_board._get_cell(1, 'c'))
        self.assertEquals('R', chess_board._get_cell(1, 'd'))
        self.assertEquals('.', chess_board._get_cell(1, 'e'))

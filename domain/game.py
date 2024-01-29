from typing import List
from config.config_wrapper import ConfigurationWrapper
from domain.special_move import SpecialMove
from domain.chess_board import ChessBoard
from domain.move import Move
from logic.move_validation_elector import get_validations_for


class Game:
    """
    A chess game
    """

    chess_board: ChessBoard
    move_history: List[Move]

    def __init__(self):
        self.chess_board = ChessBoard()
        self.move_history = []

    def get_special_moves(self) -> List[SpecialMove]:
        return [SpecialMove(move) for move in ConfigurationWrapper.get_config('special_moves') if move['enabled'] is True]

    def validate_move(self, move: Move):
        for validate_function in get_validations_for(move, self.chess_board):
            validate_function(move, self.chess_board, self.move_history)

    def make_move(self, move: Move):

        is_special_move = False
        for special_move in self.get_special_moves():
            if special_move.is_being_executed_by(move):
                special_move.validate(move)
                execute_function = special_move.create_executor(move)
                steps = execute_function(self.chess_board)
                self.move_history += steps
                is_special_move = True

        if not is_special_move:
            self.validate_move(move)
            self.chess_board.apply_move(move)
            self.move_history.append(move)

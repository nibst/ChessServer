from domain.move import Move
from domain.chess_board import ChessBoard
from typing import Callable, List
import logic.move_validations
import logic.move_constructors
import logic.move_identifiers


class SpecialMove:
    """
    A special move
    """

    name: str
    identifier: Callable[[Move, ChessBoard], bool]
    validator: Callable[[Move, ChessBoard, List[Move]], None]
    creator: Callable[[Move], Callable[[ChessBoard], List[Move]]]

    def __init__(self, configuration: dict):
        self._init_from_params(
            configuration.get('name'),
            configuration.get('identifier_func'),
            configuration.get('validator_func'),
            configuration.get('creator_func')
        )

    def _init_from_params(self, name: str, identifier_func: str, validator_func: str, creator_func: str):
        self.name = name
        self.identifier = getattr(logic.move_identifiers, identifier_func)
        self.validator = getattr(logic.move_validations, validator_func)
        self.creator = getattr(logic.move_constructors, creator_func)

    def is_being_executed_by(self, move: Move, chess_board: ChessBoard) -> bool:
        return self.identifier(move, chess_board)

    def validate(self, move: Move, chess_board: ChessBoard, move_history: List[Move]):
        self.validator(move, chess_board, move_history)

    def create_executor(self, move: Move) -> Callable[[ChessBoard], List[Move]]:
        return self.creator(move)

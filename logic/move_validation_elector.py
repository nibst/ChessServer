from typing import List, Callable
from domain.move import Move
from domain.chess_board import ChessBoard


def get_validations_for(move: Move, chess_board: ChessBoard) -> List[Callable[[Move, ChessBoard], None]]:
    """
    Get the relevant validations for this move
    """
    raise NotImplementedError()

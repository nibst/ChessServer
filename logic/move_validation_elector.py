from typing import List, Callable
from domain.move import Move
from domain.chess_board import ChessBoard
from move_validations import *

def get_validations_for(move: Move, chess_board: ChessBoard) -> List[Callable[[Move, ChessBoard], None]]:
    """
    Get the relevant validations for this move
    """
    piece = chess_board.get_cell(move.get_cell_from())
    if piece.lower() == 'k':
        return validate_king_move
    if piece.lower() == 'q':
        return validate_queen_move
    if piece.lower() == 'r':
        return validate_rook_move
    if piece.lower() == 'b':
        return validate_bishop_move
    if piece.lower() == 'n':
        return validate_horse_move
    if piece.lower() == 'p':
        return validate_pawn_move
    raise NotImplementedError()

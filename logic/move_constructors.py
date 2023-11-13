from typing import List, Callable, Tuple
from domain.chess_board import ChessBoard
from domain.move import Move


def create_castle_steps(move: Move) -> Callable[[ChessBoard], List[Move]]:
    """
    1. Create move from king to rook - 1
    2. Create move from rook to king - 1
    """

    cell_from = move.get_cell_from()
    cell_to = move.get_cell_to()
    column_diff = ord(cell_from[1]) - ord(cell_to[1])
    king_direction = int(column_diff/abs(column_diff))
    king_final_position = str(
        cell_from[0]) + chr(ord(cell_from[1]) - (2 * king_direction))
    rook_final_position = str(
        cell_to[0]) + chr(ord(king_final_position[1]) + king_direction)

    king_move = Move(
        move.get_team(),
        str(cell_from[0]) + cell_from[1],
        king_final_position,
        None
    )
    rook_move = Move(
        move.get_team(),
        str(cell_to[0]) + cell_to[1],
        rook_final_position,
        None
    )

    def perform_castle(chess_board: ChessBoard) -> List[Move]:
        chess_board.apply_move(king_move)
        chess_board.apply_move(rook_move)
        return [king_move, rook_move]

    return perform_castle


def create_en_passant_steps(move: Move) -> Callable[[ChessBoard], List[Move]]:
    """
    1. Create move from original source to captured pawn's position
    2. Create move from captured position to original destination
    """
    raise NotImplementedError()


def create_pawn_promotion_steps(move: Move) -> Callable[[ChessBoard], List[Move]]:
    """
    1. change piece to 
    """
    raise NotImplementedError()

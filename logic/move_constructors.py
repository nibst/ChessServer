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
    column_diff = ord(cell_from[0]) - ord(cell_to[0])
    king_direction = int(column_diff/abs(column_diff))
    king_final_position =  chr(ord(cell_from[0]) - (2 * king_direction)) + str(cell_from[1])
    rook_final_position = chr(ord(king_final_position[0]) + king_direction) + str(cell_to[1])

    king_move = Move(
        move.get_team(),
        cell_from[0] + str(cell_from[1]),
        king_final_position,
        None
    )
    rook_move = Move(
        move.get_team(),
        cell_to[0] + str(cell_to[1]),
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
    cell_from = move.get_cell_from()
    cell_to = move.get_cell_to()
    column_diff = ord(cell_from[0]) - ord(cell_to[0])
    pawn_horizontal_direction = int(column_diff/abs(column_diff))
    captured_pawn_position =  chr(ord(cell_from[0]) - pawn_horizontal_direction) + str(cell_from[1])

    capture_move = Move(
        move.get_team(),
        cell_from[0] + str(cell_from[1]),
        captured_pawn_position,
        None
    )
    correct_destination_move = Move(
        move.get_team(),
        captured_pawn_position,
        cell_to[0] + str(cell_to[1]),
        None
    )

    def perform_en_passant(chess_board: ChessBoard) -> List[Move]:
        chess_board.apply_move(capture_move)
        chess_board.apply_move(correct_destination_move)
        return[capture_move,correct_destination_move]
    
    return perform_en_passant


def create_pawn_promotion_steps(move: Move) -> Callable[[ChessBoard], List[Move]]:
    """
    1. change piece to 
    """
    raise NotImplementedError()

def create_il_vaticano_steps(move: Move) -> Callable[[ChessBoard], List[Move]]:
    """
    1. Move bishop (bottom or right bishop) to adjacent captured pawn position 
    2. Move bishop (bottom or right bishop) to the other adjacent pawn position
    3. Move the bishop that was not moved to the other bishops original position
    4. Move the bishop that has captured the pawns to the original position of the bishop in previous step

    Steps 1-2, capture the pawns
    Steps 3-4, swap bishops original position ()
    """
    cell_from = move.get_cell_from()
    cell_to = move.get_cell_to()    
    is_vertical:bool = False
    is_horizontal:bool = False
    #check if is vertical il vaticano
    if cell_from[0] == cell_to[0]:
        is_vertical = True
    #check if is horizontal il vaticano
    if cell_from[1] == cell_to[1]:
        is_horizontal = True

    raise NotImplementedError()
    
    def perform_il_vaticano(chess_board: ChessBoard) -> List[Move]:
        pass

    return perform_il_vaticano



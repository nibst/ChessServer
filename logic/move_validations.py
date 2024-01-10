import copy
from typing import List, Tuple
from domain.chess_board import ChessBoard
from domain.move import Move
from domain.teams import TeamEnum
from exception.illegal_move_exception import IllegalMoveException
from exception.no_king_exception import NoKingException
from logic.move_constructors import create_en_passant_steps

def _is_safe_diagonally(cell: Tuple[str, int], team: str, chess_board: ChessBoard) -> bool:
    diagonal_threats = TeamEnum[team].get_diagonal_threats()
    direction_operations = [[-1, -1], [-1, 1], [1, -1], [1, 1]]

    for direction in direction_operations:
        checked_cell = cell
        while chess_board.is_in_bounds(checked_cell):
            piece = chess_board.get_cell(checked_cell)
            if piece != '.' and piece.lower() != 'k':
                if piece in diagonal_threats:
                    return False
                else:
                    break
            checked_cell = tuple(
                [chr(ord(checked_cell[0]) + direction[0]),
                 checked_cell[1] + direction[1]]
            )

    return True


def _is_safe_orthogonally(cell: Tuple[str, int], team: str, chess_board: ChessBoard) -> bool:
    orthogonal_threats = TeamEnum[team].get_orthogonal_threats()
    direction_operations = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    for direction in direction_operations:
        checked_cell = cell
        while chess_board.is_in_bounds(checked_cell):
            piece = chess_board.get_cell(checked_cell)
            if piece != '.' and piece.lower() != 'k':
                if piece in orthogonal_threats:
                    return False
                else:
                    break
            checked_cell = tuple(
                [chr(ord(checked_cell[0]) + direction[0]),
                 checked_cell[1] + direction[1]]
            )

    return True


def _is_safe_from_pawns(cell: Tuple[str, int], team: str, chess_board: ChessBoard) -> bool:
    front = TeamEnum[team].get_front_direction()
    direction_operations = [[front, -1], [front, 1]]
    checked_cell = cell
    for direction in direction_operations:
        checked_cell = tuple(
            [chr(ord(cell[0]) + direction[0]), cell[1] + direction[1] ]
        )
        if chess_board.is_in_bounds(checked_cell) \
                and chess_board.get_cell(checked_cell) == TeamEnum[team].get_opponent_pawn_key():
            return False

    return True


def _is_safe_from_knights(cell: Tuple[str, int], team: str, chess_board: ChessBoard) -> bool:
    direction_operations = [[2, -1], [2, 1], [-2, -1], [-2, 1],
                            [1, -2], [1, 2], [-1, -2], [-1, 2]]

    checked_cell = cell
    for direction in direction_operations:
        checked_cell = tuple(
            [chr(ord(cell[0]) + direction[0]), cell[1] + direction[1]]
        )
        if chess_board.is_in_bounds(checked_cell) \
                and chess_board.get_cell(checked_cell) == TeamEnum[team].get_opponent_knight_key():
            return False

    return True


def is_in_check(cell: Tuple[str, int], team: str, chess_board: ChessBoard) -> bool:
    """
    To verify if piece is in check:
    1. Check if orthogonally there are any rooks/queens
    2. Check if diagonally there are any bishops/queens
    3. Check if in 'front' diagonally there are any pawns
    4. Check if in L there are any knights
    """

    return not (
        _is_safe_diagonally(cell, team, chess_board)
        and _is_safe_orthogonally(cell, team, chess_board)
        and _is_safe_from_pawns(cell, team, chess_board)
        and _is_safe_from_knights(cell, team, chess_board))

def _get_king_cell(team:str, chess_board:ChessBoard):
    if team == TeamEnum.BLACKS.value:
        king_piece = 'k'
    else:
        king_piece = 'K'
    columns = ['a','b','c','d','e','f','g']
    rows = [1,2,3,4,5,6,7,8]
    for row in rows:
        for column in columns:
            cell = tuple([column,row])
            piece = chess_board.get_cell(cell)
            if piece == king_piece:
                return cell
        
    #I dont know if is possible to get here
    raise NoKingException(f'There is no {team} king on the board')

def is_king_in_check(team, chess_board:ChessBoard):
    cell = _get_king_cell(team,chess_board)
    return is_in_check(cell,team,chess_board)

def validate_castle(move: Move, chess_board: ChessBoard, move_history: List[Move]):
    """
    Castle conditions:
    1. King cannot have moved
    2. Rook cannot have moved
    3. King cannot be in check
    4. King cannot pass over check
    5. No pieces in between
    """
    king_starting_cell = TeamEnum[move.get_team()].get_starting_king_cell()
    rook_starting_cell = move.get_cell_to()
    cell_from = move.get_cell_from()
    cell_to = move.get_cell_to()

    king_moved = len(
        [move for move in move_history if move.get_cell_from() == king_starting_cell]
    ) > 0
    if king_moved:
        raise IllegalMoveException(
            'King has already moved, you cannot castle!')

    rook_moved = len(
        [move for move in move_history if move.get_cell_from() == rook_starting_cell]
    ) > 0
    if rook_moved:
        raise IllegalMoveException(
            'Rook has already moved, you cannot castle!')

    if is_in_check(cell_from, move.get_team(), chess_board):
        raise IllegalMoveException('You are in check, you cannot castle!')

    starting_cell = cell_from \
        if ord(cell_from[0]) < ord(cell_to[0]) \
        else cell_to

    ending_cell = cell_from \
        if ord(cell_from[0]) > ord(cell_to[0]) \
        else cell_to

    for column in range(ord(starting_cell[0]) + 1, ord(ending_cell[0])):
        if abs(ord(cell_from[0]) - column) <= 2:
            checked_cell = tuple([chr(column), starting_cell[1]])
            if chess_board.get_cell(checked_cell) != '.':
                raise IllegalMoveException(
                    'There are pieces in the way, you cannot castle!')
            if is_in_check(checked_cell, move.get_team(), chess_board):
                raise IllegalMoveException(
                    'You are passing over check, you cannot castle!')


def validate_en_passant(move: Move, chess_board: ChessBoard, move_history: List[Move]):
    """
    En passant conditions:
    1. Capturing pawn moved 3 rank forward
    2. Captured pawn moved two squares in one move
    3. Captured pawn must have moved in the previous move
    (I think the first condition will be a consequence of the second and third condition)
    """
    cell_from = move.get_cell_from()
    cell_to = move.get_cell_to()
    captured_pawn_position:Tuple[str,int] = tuple([cell_to[0],  cell_from[1]]) 
    try:
        last_move = move_history[-1]
    except:
        raise IllegalMoveException('Pawn to be captured did not move in the previous move')
    if last_move.get_cell_to() != captured_pawn_position:
        raise IllegalMoveException('Pawn to be captured did not move in the previous move')
    moved_squares_by_captured_pawn_last_move = abs(last_move.get_cell_to()[1] - last_move.get_cell_from()[1])
    captured_pawn_moved_two_squares:bool = moved_squares_by_captured_pawn_last_move == 2
    if not captured_pawn_moved_two_squares:
        raise IllegalMoveException('Pawn to be captured did not move two squares in previous move')
    chess_board_after_en_passant = copy.deepcopy(chess_board) 
    execute_en_passant = create_en_passant_steps(move)
    execute_en_passant(chess_board_after_en_passant)
    if is_king_in_check(move.get_team(),chess_board_after_en_passant):
        raise IllegalMoveException('You will put yourself in check, you cannot en passant')



def validate_pawn_promotion(move: Move, chess_board: ChessBoard, move_history: List[Move]):
    """
    Pawn promotion conditions:
    1. Pawn must be reaching last row
    2. Chosen piece must be provided in the move's additional data
    3. Chosen piece must be of pawn's team
    4. Chosen piece must be one of the possible pieces
    """
    possible_promotion_pieces = ['q','r','b','n']
    direction = 1 if move.get_team() == TeamEnum.WHITES.value else -1
    cell_to = move.get_cell_to()
    cell_from = move.get_cell_from()
    is_reaching_last_row = (direction == 1 and cell_to[1] == 8) \
                        or (direction == -1 and cell_to[1] == 1)
    if not is_reaching_last_row:
        raise IllegalMoveException('Cannot promote without being on last row')
    piece_to_promote = move.get_additional_data()
    if piece_to_promote == None or piece_to_promote.lower() not in possible_promotion_pieces :
        raise IllegalMoveException('Cannot promote to a non-existing piece')
    is_promoting_to_opposite_team = (piece_to_promote.isupper() and move.get_team() != TeamEnum.WHITES.value) \
                                 or (piece_to_promote.islower() and move.get_team() != TeamEnum.BLACKS.value)
    if is_promoting_to_opposite_team:
        raise IllegalMoveException('Cannot promote to piece of opposite team')
    is_not_a_pawn = chess_board.get_cell(cell_from).lower() != 'p' 
    if is_not_a_pawn:
        raise IllegalMoveException('Cannot promote using a piece that is not a pawn')   

def validate_il_vaticano(move: Move, chess_board: ChessBoard, move_history: List[Move]):
    """
    Il Vaticano conditions:
    1. Two enemy pawns between two ally bishops vertically or horizontally
    """
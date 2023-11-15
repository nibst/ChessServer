from typing import List, Tuple
from domain.chess_board import ChessBoard
from domain.move import Move
from domain.teams import TeamEnum
from exception.illegal_move_exception import IllegalMoveException


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
    """
    raise NotImplementedError()


def validate_pawn_promotion(move: Move, chess_board: ChessBoard, move_history: List[Move]):
    """
    Pawn promotion conditions:
    1. Pawn must be reaching last row
    2. Chosen piece must be provided in the move's additional data
    """
    raise NotImplementedError()

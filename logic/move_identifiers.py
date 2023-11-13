from domain.teams import TeamEnum
from domain.move import Move
from domain.chess_board import ChessBoard

def is_en_passant(move: Move, chess_board: ChessBoard) -> bool:
    raise NotImplementedError()


def is_castle(move: Move, chess_board: ChessBoard) -> bool:
    cell_from = move.get_cell_from()
    cell_to = move.get_cell_to()
    moved_piece = chess_board.get_cell(cell_from)
    eaten_piece = chess_board.get_cell(cell_to)
    from_team = TeamEnum.WHITES.value if moved_piece.isupper() else TeamEnum.BLACKS.value
    to_team = TeamEnum.WHITES.value if eaten_piece.isupper() else TeamEnum.BLACKS.value
    vertical_distance = abs(cell_from[0] - cell_to[0])
    king_starting_cell = TeamEnum[move.get_team()].get_starting_king_cell()
    rook_starting_cells = TeamEnum[move.get_team()].get_starting_rook_cells()

    return not (moved_piece.lower() != 'k' or eaten_piece.lower() != 'r') \
        and not vertical_distance != 0 \
        and from_team == to_team \
        and cell_from == king_starting_cell \
        and cell_to in rook_starting_cells


def is_pawn_promotion(move: Move, chess_board: ChessBoard) -> bool:

    direction = 1 if move.get_team() == TeamEnum.WHITES.value else -1
    cell_from = move.get_cell_from()
    cell_to = move.get_cell_to()
    eaten_piece = chess_board.get_cell(cell_to)
    lateral_distance = abs(ord(cell_from[1]) - ord(cell_to[1]))
    vertical_distance = abs(cell_from[0] - cell_to[0])

    return not chess_board.get_cell(move.get_cell_from()).lower() != 'p' \
        and not ((direction > 0 and cell_to[0] < 8) or (direction < 0 and cell_to[0] > 1)) \
        and not (eaten_piece != '.' and lateral_distance == 0) \
        and not (lateral_distance > 1 or vertical_distance > 1)

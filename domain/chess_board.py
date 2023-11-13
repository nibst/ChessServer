from typing import List, Tuple
from domain.move import Move

from exception.illegal_move_exception import IllegalMoveException

BOARD_LENGHT = 8
DEFAULT_CHESS_BOARD = \
    "R N B Q K B N R;" + \
    "P P P P P P P P;" + \
    ". . . . . . . .;" + \
    ". . . . . . . .;" + \
    ". . . . . . . .;" + \
    ". . . . . . . .;" + \
    "p p p p p p p p;" + \
    "r n b q k b n r"


class ChessBoard:
    """
    A chess board
    """

    board: List[List[str]]

    def __init__(self):
        rows = DEFAULT_CHESS_BOARD.split(';')
        self.board = [[cell.strip() for cell in row.split(' ')]
                      for row in rows]

    def _convert_row_to_index(self, row: int) -> int:
        index = row - 1
        if index >= BOARD_LENGHT or index < 0:
            raise IllegalMoveException(f'Invalid row: {row}')
        return index

    def _convert_col_to_index(self, col: str) -> int:
        index = ord(col.upper()) - 65
        if index >= BOARD_LENGHT or index < 0:
            raise IllegalMoveException(f'Invalid column: {col}')
        return index

    def is_in_bounds(self, cell: Tuple[str, int]) -> bool:
        try:
            self._convert_row_to_index(cell[1])
            self._convert_col_to_index(cell[0])
            return True
        except IllegalMoveException:
            return False

    def get_cell(self, cell: Tuple[str, int]) -> str:
        return self._get_cell(cell[0], cell[1])

    def _get_cell(self, col: str, row: int,) -> str:
        row_index = self._convert_row_to_index(row)
        col_index = self._convert_col_to_index(col)
        return self.board[row_index][col_index]

    def set_cell(self, cell: Tuple[str, int], piece: str):
        self._set_cell(cell[0], cell[1], piece)

    def _set_cell(self, col: str, row: int, piece: str):
        row_index = self._convert_row_to_index(row)
        col_index = self._convert_col_to_index(col)
        self.board[row_index][col_index] = piece

    def apply_move(self, move: Move) -> str:
        """
        Returns the piece at the destination
        """
        moved_piece = self.get_cell(move.get_cell_from())
        destination_piece = self.get_cell(move.get_cell_to())
        self.set_cell(move.get_cell_to(), moved_piece)
        self.set_cell(move.get_cell_from(), '.')
        return destination_piece

    def to_string(self) -> str:
        return ('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[::-1]]))

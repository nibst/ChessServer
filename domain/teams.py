from enum import Enum
from typing import List, Tuple


class TeamEnum(Enum):
    WHITES = "WHITES"
    BLACKS = "BLACKS"

    def get_starting_king_cell(self) -> Tuple[int, str]:
        if self.value == "WHITES":
            return tuple([1, 'e'])
        else:
            return tuple([8, 'e'])

    def get_starting_rook_cells(self) -> List[Tuple[int, str]]:
        if self.value == "WHITES":
            return [tuple([1, 'h']), tuple([1, 'a'])]
        else:
            return [tuple([8, 'h']), tuple([8, 'a'])]

    def get_orthogonal_threats(self) -> List[str]:
        if self.value == "BLACKS":
            return ['Q', 'R']
        else:
            return ['q', 'r']

    def get_diagonal_threats(self) -> List[str]:
        if self.value == "BLACKS":
            return ['Q', 'B']
        else:
            return ['q', 'b']

    def get_front_direction(self) -> int:
        if self.value == "WHITES":
            return 1
        else:
            return -1

    def get_opponent_pawn_key(self) -> str:
        if self.value == "BLACKS":
            return 'P'
        else:
            return 'p'

    def get_opponent_knight_key(self) -> str:
        if self.value == "BLACKS":
            return 'N'
        else:
            return 'n'

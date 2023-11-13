from enum import Enum
from typing import List, Tuple


class TeamEnum(Enum):
    WHITES = "WHITES"
    BLACKS = "BLACKS"

    def get_starting_king_cell(self) -> Tuple[str, int]:
        if self.value == "WHITES":
            return tuple(['e', 1])
        else:
            return tuple(['e', 8])

    def get_starting_rook_cells(self) -> List[Tuple[str, int]]:
        if self.value == "WHITES":
            return [tuple(['h', 1]), tuple(['a', 1,])]
        else:
            return [tuple(['h', 8]), tuple(['a', 8])]

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

from typing import Tuple

from exception.illegal_move_exception import IllegalMoveException


class Move:
    """
    A move by a player
    """

    team: str
    from_cell: Tuple[str, int]
    to_cell: Tuple[str, int]
    additional_data: str

    def __init__(self, team, from_cell: str, to_cell: str, additional_data: str):

        if len(from_cell) != 2 or from_cell[0].isnumeric() or not from_cell[1].isnumeric():
            raise IllegalMoveException(f'Invalid move origin: {from_cell}')

        if len(to_cell) != 2 or to_cell[0].isnumeric() or not to_cell[1].isnumeric():
            raise IllegalMoveException(f'Invalid move destination: {to_cell}')

        self.team = team
        self.from_cell = tuple([from_cell[0].lower(), int(from_cell[1])])
        self.to_cell = tuple([ to_cell[0].lower(), int(to_cell[1])])
        self.additional_data = additional_data

    def get_team(self) -> str:
        return self.team

    def get_cell_from(self) -> Tuple[str, int]:
        return self.from_cell

    def get_cell_to(self) -> Tuple[str, int]:
        return self.to_cell

    def get_additional_data(self) -> str:
        return self.additional_data

from azul.board import Board
from azul.color import Color
from azul.factory import Factory
from azul.pattern_line import PatternLine
from azul.table import Table


class Player:
    _next_id: int = 1

    def __init__(self, table: Table) -> None:
        self._active: bool = False
        self._board: Board = Board(table.lid)
        self._id: int = Player._next_id
        Player._next_id += 1
        self._score: int = 0
        self._table: Table = table

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        self._active = value

    @property
    def board(self) -> Board:
        return self._board

    @property
    def id_(self) -> int:
        return self._id

    @property
    def score(self) -> int:
        return self._score

    def move_tiles(self) -> None:
        for i, line in enumerate(self._board.pattern_lines):
            if line.is_complete():
                self._score += self._board.wall.place_tile(
                    line.slots[-1].remove_tile(), row=i
                )
                for slot in line.slots:
                    self._table.lid.place_tile(slot.remove_tile())
        self._score -= self._board.floor_line.remove_tiles()

    def pick_tiles_from_factory(
        self, factory: Factory, color: Color, pattern_line: PatternLine
    ) -> None:
        picked = self._table.pick_from_factory(factory=factory, color=color)
        excess = pattern_line.place_tiles(tiles=picked)
        self._board.floor_line.place_tiles(tiles=excess)

    def pick_tiles_from_table_center(
        self, color: Color, pattern_line: PatternLine
    ) -> None:
        picked = self._table.pick_from_center(color=color)
        excess = pattern_line.place_tiles(tiles=picked)
        self._board.floor_line.place_tiles(tiles=excess)

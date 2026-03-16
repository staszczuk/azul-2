from azul.board import Board
from azul.color import Color
from azul.lid import Lid
from azul.supplier import Supplier


class Player:
    def __init__(self, name: str) -> None:
        self._board = Board()
        self._name = name
        self._points = 0

    @property
    def board(self) -> Board:
        return self._board

    @property
    def name(self) -> str:
        return self._name

    @property
    def points(self) -> int:
        return self._points

    def add_points(self, points: int) -> None:
        self._points += points

    def move_tiles(self, lid: Lid) -> int:
        points = 0
        for i, pattern_line in enumerate(self._board.pattern_lines):
            if pattern_line.is_complete():
                points += self._board.wall.place_tile(
                    pattern_line.take_rightmost_tile(), i
                )
                lid.place_tiles(pattern_line.take_all_tiles())
        points += self._board.floor_line.sum_points()
        if points < 0:
            points = 0
        return points

    def pick_tiles(self, supplier: Supplier, color: Color, pattern_line_i: int) -> None:
        pattern_line = self.board.pattern_lines[pattern_line_i]
        for tile in supplier.pick_tiles(color):
            if not pattern_line.is_complete() and tile.color:
                pattern_line.place_tile(tile)
            else:
                self._board.floor_line.place_tile(tile)

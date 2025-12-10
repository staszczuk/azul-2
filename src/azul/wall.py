import collections

from azul.color import Color
from azul.slot import Slot
from azul.tile import Tile

FIRST_ROW_COLOR_ORDER = [Color.BLUE, Color.YELLOW, Color.RED, Color.BLACK, Color.WHITE]


class Wall:
    def __init__(self) -> None:
        self._lines: list[list[Slot]] = []
        color_order = collections.deque(FIRST_ROW_COLOR_ORDER)
        for _ in range(5):
            self._lines.append([Slot(color) for color in color_order])
            color_order.rotate(1)

    @property
    def lines(self) -> list[list[Slot]]:
        return self._lines

    def check_win_condition(self) -> bool:
        return any(all(not slot.is_empty() for slot in line) for line in self._lines)

    def place_tile(self, tile: Tile, line_i: int) -> int:
        for i, slot in enumerate(self._lines[line_i]):
            if slot.color == tile.color:
                slot.place_tile(tile)
                return self._calculate_points(line_i, i)
        raise Exception

    def _calculate_points(self, row: int, col: int) -> int:
        points = 1
        c = col - 1
        while c >= 0 and not self._lines[row][c].is_empty():
            points += 1
            c -= 1
        c = col + 1
        while c < len(self._lines[row]) and not self._lines[row][c].is_empty():
            points += 1
            c += 1
        r = row - 1
        while r >= 0 and not self._lines[r][col].is_empty():
            points += 1
            r -= 1
        r = row + 1
        while r < len(self._lines) and not self._lines[r][col].is_empty():
            points += 1
            r += 1
        return points

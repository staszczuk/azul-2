from collections import deque

from azul.color import Color
from azul.slot import Slot
from azul.tile import Tile


class Wall:
    def __init__(self) -> None:
        self._slots: list[list[Slot]] = []
        color_order = deque(
            [Color.BLUE, Color.YELLOW, Color.RED, Color.BLACK, Color.WHITE]
        )
        for _ in range(5):
            self._slots.append([])
            for color in color_order:
                self._slots[-1].append(Slot(color=color))
            color_order.rotate(1)

    @property
    def slots(self) -> list[list[Slot]]:
        return self._slots

    def place_tile(self, tile: Tile, row: int) -> int:
        points = 0
        for i, slot in enumerate(self._slots[row]):
            if slot.color == tile.color:
                slot.tile = tile
                points = self._calculate_points(row=row, col=i)
        return points

    def _calculate_points(self, row: int, col: int) -> int:
        points = 1
        c = col - 1
        while c >= 0 and self.slots[row][c].is_not_empty():
            points += 1
            c -= 1
        c = col + 1
        while c < len(self.slots[row]) and self.slots[row][c].is_not_empty():
            points += 1
            c += 1
        r = row - 1
        while r >= 0 and self.slots[r][col].is_not_empty():
            points += 1
            r -= 1
        r = row + 1
        while r < len(self.slots) and self.slots[r][col].is_not_empty():
            points += 1
            r += 1
        return points

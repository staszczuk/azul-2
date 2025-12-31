from azul.fl_slot import FLSlot
from azul.tile import Tile


class FloorLine:
    def __init__(self) -> None:
        self._slots = [FLSlot(None, points) for points in [-1, -1, -2, -2, -2, -3, -3]]

    @property
    def slots(self) -> list[FLSlot]:
        return self._slots

    def place_tile(self, tile: Tile) -> None:
        for slot in self._slots:
            if slot.is_empty():
                slot.place_tile(tile)
                break

    def sum_points(self) -> int:
        points = 0
        for slot in self._slots:
            if not slot.is_empty():
                points += slot.points
        return points

    def take_all_tiles(self) -> list[Tile]:
        return [slot.take_tile() for slot in self._slots if not slot.is_empty()]

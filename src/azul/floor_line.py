from azul.floor_line_slot import FloorLineSlot
from azul.lid import Lid
from azul.tile import Tile


class FloorLine:
    def __init__(self, lid: Lid) -> None:
        self._lid: Lid = lid
        self._slots: list[FloorLineSlot] = [
            FloorLineSlot(points=points) for points in [1, 1, 2, 2, 2, 3, 3]
        ]

    @property
    def slots(self) -> list[FloorLineSlot]:
        return self._slots

    def place_tiles(self, tiles: list[Tile]) -> None:
        for tile in tiles:
            for slot in self._slots:
                if slot.is_empty():
                    slot.tile = tile
                    return
            self._lid.place_tile(tile=tile)

    def remove_tiles(self) -> int:
        points = 0
        for slot in self._slots:
            if slot.is_empty():
                break
            self._lid.place_tile(slot.remove_tile())
            points += slot.points
        return points

from azul.slot import Slot
from azul.tile import Tile


class PatternLine:
    def __init__(self, slot_count: int) -> None:
        self._slots: list[Slot] = [Slot() for _ in range(slot_count)]

    @property
    def slots(self) -> list[Slot]:
        return self._slots

    def is_complete(self) -> bool:
        return all(not slot.is_empty() for slot in self._slots)

    def place_tiles(self, tiles: list[Tile]) -> list[Tile]:
        for slot in reversed(self._slots):
            if not tiles:
                break
            if slot.is_empty() and slot.color is None:
                slot.tile = tiles.pop()
        return tiles

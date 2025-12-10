from azul.slot import Slot
from azul.tile import Tile


class PatternLine:
    def __init__(self, slot_count: int) -> None:
        self._slots = [Slot(None) for _ in range(slot_count)]

    @property
    def slots(self) -> list[Slot]:
        return self._slots

    def is_complete(self) -> bool:
        return all(not slot.is_empty() for slot in self._slots)

    def place_tile(self, tile: Tile) -> None:
        empty_slots = [slot for slot in self._slots if slot.is_empty()]
        if len(empty_slots) == len(self._slots):
            for slot in self._slots:
                slot.color = tile.color
        empty_slots[-1].place_tile(tile)

    def take_rightmost_tile(self) -> Tile:
        return self._slots[-1].take_tile()

    def take_all_tiles(self) -> list[Tile]:
        return [slot.take_tile() for slot in self._slots if not slot.is_empty()]

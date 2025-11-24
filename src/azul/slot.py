from azul.color import Color
from azul.tile import Tile


class Slot:
    def __init__(self, color: Color | None = None) -> None:
        self._color: Color | None = color
        self._tile: Tile | None = None

    @property
    def color(self) -> Color | None:
        return self._color

    @property
    def tile(self) -> Tile | None:
        return self._tile

    @tile.setter
    def tile(self, value: Tile) -> None:
        self._tile = value

    def is_empty(self) -> bool:
        return self._tile is None

    def is_not_empty(self) -> bool:
        return self._tile is not None

    def place_tile(self, tile: Tile) -> None:
        self._tile = tile

    def remove_tile(self) -> Tile:
        if self._tile is None:
            raise Exception("Slot is empty")
        self._tile, tile = None, self._tile
        return tile

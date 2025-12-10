from azul.color import Color
from azul.tile import Tile


class Slot:
    def __init__(self, color: Color | None) -> None:
        self._color = color
        self._tile: Tile | None = None

    @property
    def color(self) -> Color | None:
        return self._color

    @property
    def tile(self) -> Tile | None:
        return self._tile

    @color.setter
    def color(self, value: Color | None) -> None:
        self._color = value

    def is_empty(self) -> bool:
        return self._tile is None

    def place_tile(self, tile: Tile) -> None:
        self._color = tile.color
        self._tile = tile

    def take_tile(self) -> Tile:
        if self._tile is None:
            raise Exception
        self._color = None
        self._tile, tile = None, self._tile
        return tile

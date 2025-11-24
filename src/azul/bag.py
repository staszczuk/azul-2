import random

from azul.color import Color
from azul.tile import Tile


class Bag:
    def __init__(self) -> None:
        self._tiles: list[Tile] = []
        for color in Color:
            self._tiles.extend(Tile(color=color) for _ in range(20))
        random.shuffle(self._tiles)

    @property
    def tiles(self) -> list[Tile]:
        return self._tiles

    def draw(self) -> Tile:
        return self._tiles.pop()

    def fill(self, tiles: list[Tile]) -> None:
        self.tiles.extend(tiles)

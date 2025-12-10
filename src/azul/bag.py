import random

from azul.color import Color
from azul.tile import Tile


class Bag:
    def __init__(self) -> None:
        self._tiles = [Tile(color) for color in Color for _ in range(20)]
        random.shuffle(self._tiles)

    def draw_tile(self) -> Tile:
        return self._tiles.pop()

    def refill(self, tiles: list[Tile]) -> None:
        self._tiles.extend(tiles)

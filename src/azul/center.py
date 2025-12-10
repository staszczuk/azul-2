from azul.color import Color
from azul.supplier import Supplier
from azul.tile import Tile


class Center(Supplier):
    def __init__(self) -> None:
        super().__init__()
        self._tiles: list[Tile] = [Tile(None)]

    @property
    def tiles(self) -> list[Tile]:
        return self._tiles

    def is_empty(self) -> bool:
        return len(self._tiles) == 0

    def pick_tiles(self, color: Color) -> list[Tile]:
        tiles = [tile for tile in self._tiles if tile.color in [color, None]]
        self._tiles[:] = [
            tile for tile in self._tiles if tile.color not in [color, None]
        ]
        return tiles

    def place_tile(self, tile: Tile) -> None:
        self._tiles.append(tile)

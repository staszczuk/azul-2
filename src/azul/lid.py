from azul.tile import Tile


class Lid:
    def __init__(self) -> None:
        self._tiles: list[Tile] = []

    @property
    def tiles(self) -> list[Tile]:
        return self._tiles

    def place_tile(self, tile: Tile) -> None:
        self._tiles.append(tile)

    def remove_tiles(self) -> list[Tile]:
        self._tiles, tiles = [], self._tiles
        return tiles

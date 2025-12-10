from azul.tile import Tile


class Lid:
    def __init__(self) -> None:
        self._tiles: list[Tile] = []

    def place_tile(self, tile: Tile) -> None:
        self._tiles.append(tile)

    def place_tiles(self, tiles: list[Tile]) -> None:
        self._tiles.extend(tiles)

    def take_all_tiles(self) -> list[Tile]:
        tiles, self._tiles = self._tiles, []
        return tiles

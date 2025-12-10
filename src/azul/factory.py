from azul.bag import Bag
from azul.center import Center
from azul.color import Color
from azul.supplier import Supplier
from azul.tile import Tile


class Factory(Supplier):
    def __init__(self, bag: Bag, center: Center) -> None:
        super().__init__()
        self._center = center
        self._tiles = [bag.draw_tile() for _ in range(4)]

    @property
    def tiles(self) -> list[Tile]:
        return self._tiles

    def is_empty(self) -> bool:
        return len(self._tiles) == 0

    def pick_tiles(self, color: Color) -> list[Tile]:
        tiles: list[Tile] = []
        for tile in self._tiles:
            if tile.color == color:
                tiles.append(tile)
            else:
                self._center.place_tile(tile)
        self._tiles.clear()
        return tiles

    def refill(self, bag: Bag) -> None:
        while len(self._tiles) != 4:
            self._tiles.append(bag.draw_tile())

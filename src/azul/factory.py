from azul.bag import Bag
from azul.tile import Tile


class Factory:
    _next_id: int = 0

    def __init__(self, bag: Bag) -> None:
        self._id: int = Factory._next_id
        Factory._next_id += 1
        self._tiles: list[Tile] = [bag.draw() for _ in range(4)]

    @property
    def id_(self) -> int:
        return self._id

    @property
    def tiles(self) -> list[Tile]:
        return self._tiles

    def pick(self) -> list[Tile]:
        self._tiles, picked = [], self._tiles
        return picked

from abc import abstractmethod

from azul.color import Color
from azul.tile import Tile


class Supplier:
    _next_id = 0

    def __init__(self) -> None:
        self._supplier_id = Supplier._next_id
        Supplier._next_id += 1

    @property
    def supplier_id(self) -> int:
        return self._supplier_id

    @abstractmethod
    def pick_tiles(self, color: Color) -> list[Tile]:
        pass

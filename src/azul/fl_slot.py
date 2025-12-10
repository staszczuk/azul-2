from azul.color import Color
from azul.slot import Slot


class FLSlot(Slot):
    def __init__(self, color: Color | None, points: int) -> None:
        super().__init__(color)
        self._points = points

    @property
    def points(self) -> int:
        return self._points

    def place_sp_tile(self) -> None:
        self._has_sp_tile = True

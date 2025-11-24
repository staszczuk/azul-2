from azul.slot import Slot


class FloorLineSlot(Slot):
    def __init__(self, points: int) -> None:
        super().__init__(color=None)
        self._points: int = points

    @property
    def points(self) -> int:
        return self._points

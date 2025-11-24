from azul.color import Color


class Tile:
    _next_id = 0

    def __init__(self, color: Color) -> None:
        self._color: Color = color
        self._id: int = Tile._next_id
        Tile._next_id += 1

    @property
    def color(self) -> Color:
        return self._color

    @property
    def id_(self) -> int:
        return self._id

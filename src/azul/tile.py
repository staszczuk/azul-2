from azul.color import Color


class Tile:
    _next_id = 0

    def __init__(self, color: Color | None) -> None:
        self._color: Color | None = color
        self._id = Tile._next_id
        Tile._next_id += 1

    @property
    def color(self) -> Color | None:
        return self._color

    @property
    def id_(self) -> int:
        return self._id

from azul.floor_line import FloorLine
from azul.pattern_line import PatternLine
from azul.wall import Wall


class Board:
    def __init__(self) -> None:
        self._floor_line = FloorLine()
        self._pattern_lines = [PatternLine(i) for i in range(1, 6)]
        self._wall = Wall()

    @property
    def floor_line(self) -> FloorLine:
        return self._floor_line

    @property
    def pattern_lines(self) -> list[PatternLine]:
        return self._pattern_lines

    @property
    def wall(self) -> Wall:
        return self._wall

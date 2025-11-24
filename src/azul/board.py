from azul.floor_line import FloorLine
from azul.lid import Lid
from azul.pattern_line import PatternLine
from azul.wall import Wall


class Board:
    def __init__(self, lid: Lid) -> None:
        self._pattern_lines: list[PatternLine] = [
            PatternLine(slot_count=i) for i in range(1, 6)
        ]
        self._wall: Wall = Wall()
        self._floor_line: FloorLine = FloorLine(lid)

    @property
    def floor_line(self) -> FloorLine:
        return self._floor_line

    @property
    def pattern_lines(self) -> list[PatternLine]:
        return self._pattern_lines

    @property
    def wall(self) -> Wall:
        return self._wall

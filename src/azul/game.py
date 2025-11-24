from azul.player import Player
from azul.table import Table


class Game:
    def __init__(self, player_count: int) -> None:
        self._table: Table = Table(player_count=player_count)
        self._players: list[Player] = [
            Player(table=self._table) for _ in range(player_count)
        ]

    @property
    def players(self) -> list[Player]:
        return self._players

    @property
    def table(self) -> Table:
        return self._table

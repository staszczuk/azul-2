from azul.color import Color
from azul.player import Player
from azul.table import Table


class Game:
    def __init__(self, players: list[Player]) -> None:
        self._players = players
        self._current_player_i = 0
        self._round = 0
        self._table = Table(len(players))

    @property
    def current_player(self) -> Player:
        return self._players[self._current_player_i]

    @property
    def players(self) -> list[Player]:
        return self._players

    @property
    def table(self) -> Table:
        return self._table

    def take_turn(self, supplier_id: int, color: Color, pattern_line_i: int) -> None:
        supplier = self._table.get_supplier(supplier_id)
        self.current_player.pick_tiles(supplier, color, pattern_line_i)
        if self._table.are_all_suppliers_empty():
            self._move_tiles()
            if self._check_end():
                for player in self._players:
                    print(player.name, player.points)
                return
            self._prepare_next_round()
            self._round += 1
        else:
            self._switch_player()

    def _check_end(self) -> bool:
        return any(player.board.wall.check_win_condition() for player in self._players)

    def _move_tiles(self) -> None:
        for player in self._players:
            player.add_points(player.move_tiles(self._table.lid))

    def _prepare_next_round(self) -> None:
        for i, player in enumerate(self._players):
            for tile in player.board.floor_line.take_all_tiles():
                if tile.color:
                    self._table.lid.place_tile(tile)
                else:
                    self._table.center.place_tile(tile)
                    self._current_player_i = i
        self._table.bag.refill(self._table.lid.take_all_tiles())
        for factory in self._table.factories:
            factory.refill(self._table.bag)

    def _switch_player(self) -> None:
        self._current_player_i = (self._current_player_i + 1) % len(self._players)

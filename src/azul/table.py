from azul.bag import Bag
from azul.color import Color
from azul.factory import Factory
from azul.lid import Lid
from azul.tile import Tile


class Table:
    def __init__(self, player_count: int) -> None:
        self._bag: Bag = Bag()
        self._center: list[Tile] = []
        factory_count: int
        match player_count:
            case 2:
                factory_count = 5
            case 3:
                factory_count = 7
            case 4:
                factory_count = 9
            case _:
                raise Exception("Invalid factory_count value")
        self._factories: list[Factory] = [
            Factory(bag=self._bag) for _ in range(factory_count)
        ]
        self._lid: Lid = Lid()

    @property
    def bag(self) -> Bag:
        return self._bag

    @property
    def center(self) -> list[Tile]:
        return self._center

    @property
    def factories(self) -> list[Factory]:
        return self._factories

    @property
    def lid(self) -> Lid:
        return self._lid

    def pick_from_center(self, color: Color) -> list[Tile]:
        return [tile for tile in self._center if tile.color == color]

    def pick_from_factory(self, factory: Factory, color: Color) -> list[Tile]:
        picked: list[Tile] = []
        for tile in factory.pick():
            if tile.color == color:
                picked.append(tile)
            else:
                self._center.append(tile)
        return picked

    def refill_bag(self) -> None:
        self._bag.fill(self._lid.remove_tiles())

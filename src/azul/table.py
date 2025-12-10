from azul.bag import Bag
from azul.center import Center
from azul.factory import Factory
from azul.lid import Lid
from azul.supplier import Supplier


class Table:
    def __init__(self, player_count: int) -> None:
        self._bag = Bag()
        self._center = Center()
        factory_count = self._get_factory_count(player_count)
        self._factories = [
            Factory(self._bag, self._center) for _ in range(factory_count)
        ]
        self._lid = Lid()

    @property
    def bag(self) -> Bag:
        return self._bag

    @property
    def center(self) -> Center:
        return self._center

    @property
    def factories(self) -> list[Factory]:
        return self._factories

    @property
    def lid(self) -> Lid:
        return self._lid

    def are_all_suppliers_empty(self) -> bool:
        return self._center.is_empty() and all(
            factory.is_empty() for factory in self._factories
        )

    def get_supplier(self, id_: int) -> Supplier:
        if self._center.supplier_id == id_:
            return self._center
        for factory in self._factories:
            if factory.supplier_id == id_:
                return factory
        raise Exception

    def _get_factory_count(self, player_count: int) -> int:
        match player_count:
            case 2:
                return 5
            case 3:
                return 7
            case 4:
                return 9
            case _:
                raise Exception

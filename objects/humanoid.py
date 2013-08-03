from rechargeable import Rechargeable
from movable_object import Movable_Object
from inventory_owner import Inventory_Owner


class Humanoid(Movable_Object, Inventory_Owner):
    def __init__(self, **kwargs):
        self.hp = Rechargeable(capacity=kwargs['hp'])
        self.is_alive = True
        self.name = kwargs['name']
        super(Humanoid, self).__init__(**kwargs)
        self.isPickable = False

    def get(self, game_world, sys, item):
        pass
from basic_object import Basic_Object


class Inventory_Owner(Basic_Object):
    def __init__(self, **kwargs):
        super(Inventory_Owner, self).__init__(**kwargs)
        self.inventory = []

    def pick_up_item(self, item):
        self.inventory.append(item)

    def drop_item(self, item):
        item.coordinates = self.coordinates
        self.inventory.remove(item)

    def get_inventory_info(self):
        return str(self.inventory)
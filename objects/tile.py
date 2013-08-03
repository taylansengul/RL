from basic_object import Basic_Object


class Tile(Basic_Object):
    icons = {'': '', 'wall': '#', 'floor': ' ', 'open door': '-', 'closed door': '+'}

    def __init__(self, coordinates=None, tip=''):
        kwargs = {'coordinates': coordinates, 'icon': Tile.icons[tip], 'color': 'white', 'name': tip}
        super(Tile, self).__init__(**kwargs)
        self.tip = tip
        self.explored = False
        self.isVisible = False
        self.active = False
        self.objects_ = []

    def has_objects(self):
        return self.objects_ != []

    def set_tip(self, tip):
        self.tip = tip
        self.icon = Tile.icons[tip]

    def add_object(self, object_):
        self.objects_.append(object_)

    def remove_object(self, object_):
        self.objects_.remove(object_)
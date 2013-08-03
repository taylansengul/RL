from data import Colors


class Basic_Object(object):
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.coordinates = kwargs['coordinates']
        self.icon = kwargs['icon']
        self.color = Colors.palette[kwargs['color']]

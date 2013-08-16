import data


class Text(object):
    def __init__(self, screen=None, context=None, coordinates=None, color=None, font=None):
        self.screen = screen
        self.context = context
        self.coordinates = coordinates
        if isinstance(color, str):
            self.color = data.colors.palette[color]
        else:
            self.color = color
        self.font = font
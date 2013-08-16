import data


class Text(object):
    def __init__(self, game, screen=None, context=None, coordinates=None, color=None, font='arial', font_size=12):
        self.game = game
        self.screen = screen
        self.context = context
        self.coordinates = coordinates
        if isinstance(color, str):
            self.color = data.colors.palette[color]
        else:
            self.color = color
        self.font = font
        self.font_size = font_size

    def render(self):
        self.game.graphics_engine.font_manager.Draw(self.screen.surface, self.font, self.font_size, self.context, self.coordinates,
                                                    self.color, 'left', 'top', True)
        self.screen.render()
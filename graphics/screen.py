from data import screens
import globals as g


class Screen(object):
    def __init__(self, game, **kwargs):
        self.game = game
        self.ID = str(kwargs['state']) + str(kwargs['name'])
        self.name = kwargs['name']
        self.state = kwargs['state']
        self.size = self.game.data.screens.screen_size[self.state][self.name]
        self.coordinates = self.game.data.screens.screen_coordinates[self.state][self.name]
        self.surface = self.game.pygame.Surface(self.size)

    def render(self):
        screens.MAIN.blit(self.surface, self.coordinates)

    def clear(self, color='black'):
        if isinstance(color, str):
            color = g.colors.palette[color]
        self.surface.fill(color)
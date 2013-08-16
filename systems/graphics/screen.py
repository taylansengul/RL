import data


class Screen(object):
    def __init__(self, game, **kwargs):
        self.game = game
        self.ID = kwargs['state'] + kwargs['name']
        self.name = kwargs['name']
        self.state = kwargs['state']
        self.size = data.screens.screen_size[self.state][self.name]
        self.coordinates = data.screens.screen_coordinates[self.state][self.name]
        self.surface = self.game.pygame.Surface(self.size)

    def render(self):
        self.game.graphics_engine.screens['main'].blit(self.surface, self.coordinates)

    def clear(self, color='black'):
        if isinstance(color, str):
            color = data.colors.palette[color]
        self.surface.fill(color)
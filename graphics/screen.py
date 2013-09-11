from data import screen_properties
from globals import *


class Screen(dict):
    def __init__(self, game, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.x = kwargs['left']
        self.y = kwargs['top']
        self.w = kwargs['width']
        self.h = kwargs['height']
        self.game = game
        self.surface = self.game.pygame.Surface((self.w, self.h))

    def render(self):
        screen_properties.MAIN.blit(self.surface, (self.x, self.y))

    def clear(self, color='black'):
        if isinstance(color, str):
            color = ColorID[color]
        self.surface.fill(color)
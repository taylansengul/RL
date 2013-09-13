import pygame

from globals import *
from settings import screen_settings


class Screen(object):
    if not '_MAIN' in locals():
        __MAIN_SURFACE = pygame.display.set_mode((screen_settings.width, screen_settings.height), 0, 32)
    _FILL_COLOR = BLACK

    def __init__(self, **kwargs):
        self.left = kwargs['left']
        self.top = kwargs['top']
        self.width = kwargs['width']
        self.height = kwargs['height']
        self.surface = pygame.Surface((self.width, self.height))

    def render_to_main(self):
        """render screen surface to main screen surface"""
        Screen.__MAIN_SURFACE.blit(self.surface, (self.left, self.top))

    def clear(self):
        """clear self with the default _FILL_COLOR which is black"""
        self.surface.fill(Screen._FILL_COLOR)

    @staticmethod
    def force_screen_update():
        """update the entire screen. This method should be called when there is something to be displayed before
        action is requested"""
        pygame.display.flip()

    @staticmethod
    def clear_main():
        """clear the main screen surface with the default _FILL_COLOR which is black"""
        Screen.__MAIN_SURFACE.fill(Screen._FILL_COLOR)
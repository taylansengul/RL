import pygame as pg
import data
from systems.cFontManager import cFontManager


class Graphics_Engine(object):
    def __init__(self):

        self.screens = {}

    def init(self, sys):
        sys.stateManager.currentState.init()

    def get_screen_position_of(self, (x, y)):
        c1 = data.Screens.tile_length * x
        c2 = data.Screens.tile_length * y
        c3 = data.Screens.tile_length
        return pg.Rect(c1, c2, c3, c3)

    def display_messages(self, sys):
        new_line_height = 12
        screen = self.screens['messages']
        coordinates = data.Screens.screen_coordinates[sys.stateManager.currentState.name]['messages']
        while sys.logger.has_unhandled_messages():
            sys.logger.handle_message()

        screen.fill(data.Colors.palette['black'])
        for co, message in enumerate(sys.logger.message_archive[-4:]):
            self.fontMgr.Draw(screen, 'arial', 12, message,
                              pg.Rect(0, new_line_height*co, coordinates[0],
                                      coordinates[1]), data.Colors.palette['white'], 'left', 'top', True)
        self.screens['main'].blit(screen, coordinates)

    def render_info(self, sys, info):
        for d in info:
            s_name = d['screen']
            screen = self.screens[s_name]
            coordinates = data.Screens.screen_coordinates[sys.stateManager.currentState.name][s_name]
            screen.fill(data.Colors.palette['black'])
            for i in d['info']:
                c = i['coordinates'] + (coordinates[0], coordinates[1])
                self.fontMgr.Draw(screen, 'arial', 12, i['item'], pg.Rect(c), i['color'], 'left', 'top', True)
            self.screens['main'].blit(screen, coordinates)

    def update_screen(self, sys):
        sys.stateManager.currentState.updateScreen(sys)
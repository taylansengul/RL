import pygame as pg
import data
from systems.cFontManager import cFontManager


class Graphics_Engine(object):
    def __init__(self, game):
        self.game = game
        self.screens = {}
        self.fontMgr = None  # is setup in Initializing State

    def init(self):
        self.game.state_manager.current_state.init()

    def get_screen_position_of(self, (x, y)):
        c1 = data.screens.tile_length * x
        c2 = data.screens.tile_length * y
        c3 = data.screens.tile_length
        return pg.Rect(c1, c2, c3, c3)

    def display_messages(self):
        new_line_height = 12
        screen = self.screens['messages']
        coordinates = data.screens.screen_coordinates[self.game.state_manager.current_state.id]['messages']
        while self.game.logger.has_unhandled_messages():
            self.game.logger.handle_message()

        screen.fill(data.colors.palette['black'])
        for co, message in enumerate(self.game.logger.message_archive[-4:]):
            self.fontMgr.Draw(screen, 'arial', 12, message,
                              pg.Rect(0, new_line_height*co, coordinates[0],
                                      coordinates[1]), data.colors.palette['white'], 'left', 'top', True)
        self.screens['main'].blit(screen, coordinates)

    def render_info(self, info_list):
        for a_dict in info_list:
            s_id = a_dict['screen']
            screen = self.screens[s_id]
            coordinates = data.screens.screen_coordinates[self.game.state_manager.current_state.id][s_id]
            screen.fill(data.colors.palette['black'])
            for i in a_dict['info']:
                c = i['coordinates'] + (coordinates[0], coordinates[1])
                self.fontMgr.Draw(screen, 'arial', 12, i['item'], pg.Rect(c), i['color'], 'left', 'top', True)
            self.screens['main'].blit(screen, coordinates)

    def update_screen(self):
        self.game.state_manager.current_state.updateScreen()
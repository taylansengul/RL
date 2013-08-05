import pygame as pg
import pygame.locals as pgl
import data


class Io_Handler(object):
    def __init__(self, game):
        self.game = game
        self.previous_event = None
        self.active_event = None
        self.click_coordinates = (-1, -1)
        self.hover_coordinates = (-1, -1)
        self.keyboard_commands_dictionary = {'map state': {pgl.K_i: 'inventory',
                                                           pgl.K_c: 'close door',
                                                           pgl.K_e: 'eat item',
                                                           pgl.K_g: 'pick up item',
                                                           pgl.K_d: 'drop item',
                                                           pgl.K_SPACE: 'descend',
                                                           pgl.K_RIGHT: 'move right',
                                                           pgl.K_LEFT: 'move left',
                                                           pgl.K_DOWN: 'move down',
                                                           pgl.K_UP: 'move up',
                                                           pgl.K_ESCAPE: 'quit'},
                                             'main menu state': {pgl.K_DOWN: 'down',
                                                                 pgl.K_UP: 'up',
                                                                 pgl.K_RETURN: 'select'},
                                             'game over state': {pgl.K_SPACE: 'pass'},
                                             'initializing state': {},
                                             'inventory state': {pgl.K_ESCAPE: 'quit',
                                                                 pgl.K_e: 'eat item'}}

    def compute_active_event(self):
        """compute the active event"""
        # reset variables
        self.previous_event = self.active_event  # previous event = previous active event
        self.active_event = None
        self.click_coordinates = (-1, -1)
        self.hover_coordinates = (-1, -1)
        # wait for input
        event = pg.event.wait()
        if event.type == pg.MOUSEBUTTONDOWN:  # mouse click coordinates
            x, y = event.pos
            if x < data.screens.screen_size['main'][0] and y < data.screens.screen_size['main'][1]:
                self.active_event = 'moving'
                self.click_coordinates = (x, y)
        elif event.type == pg.MOUSEMOTION:
            self.input = 'mouse motion'
            self.hover_coordinates = event.pos
        elif event.type == pgl.QUIT:
            self.active_event = 'quit'
        elif event.type == pgl.KEYDOWN:  # pressed keyboard key
            # find out the active event from keyboard commands dictionary
            keyboard = self.game.state_manager.current_state.id
            for key in self.keyboard_commands_dictionary[keyboard]:
                if event.key == key:
                    self.active_event = self.keyboard_commands_dictionary[keyboard][key]

    def get_active_event(self):
        return self.active_event

    def get_click_coordinates(self):
        return self.click_coordinates

    def get_hover_coordinates(self):
        return self.hover_coordinates

    def set_active_event(self, event):
        self.active_event = event
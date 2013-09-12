import pygame.locals as pgl
import globals as g
import settings
import pygame


class Io_Handler(object):
    def __init__(self, game):
        self.game = game
        self.previous_event = None
        self.active_event = None
        self.click_coordinates = (-1, -1)
        self.hover_coordinates = (-1, -1)
        self.keyboard_commands_dictionary = {
            g.StateID.MAP: {
                pgl.K_i: 'inventory_objects_list',
                pgl.K_c: 'close door',
                pgl.K_e: 'eat item',
                pgl.K_g: 'pick up item',
                pgl.K_d: 'drop item',
                pgl.K_t: 'target',
                pgl.K_SPACE: 'descend',
                pgl.K_RIGHT: 'right',
                pgl.K_LEFT: 'left',
                pgl.K_DOWN: 'down',
                pgl.K_UP: 'up',
                pgl.K_ESCAPE: 'quit'},
            g.StateID.MAIN_MENU: {
                pgl.K_DOWN: 'down',
                pgl.K_UP: 'up',
                pgl.K_RETURN: 'select'},
            g.StateID.GAME_OVER: {
                pgl.K_SPACE: 'pass'},
            g.StateID.INVENTORY: {
                pgl.K_DOWN: 'down',
                pgl.K_UP: 'up',
                pgl.K_RETURN: 'select',
                pgl.K_ESCAPE: 'quit',
                pgl.K_e: 'show edible items',
                pgl.K_u: 'show consumable items'},
            g.StateID.TARGETING: {
                pgl.K_RIGHT: 'right',
                pgl.K_LEFT: 'left',
                pgl.K_DOWN: 'down',
                pgl.K_UP: 'up',
                pgl.K_RETURN: 'select'}}

    def compute_active_event(self):
        """compute the active event"""
        # reset variables
        self.previous_event = self.active_event  # previous event = previous active event
        self.active_event = None
        self.click_coordinates = (-1, -1)
        self.hover_coordinates = (-1, -1)
        # wait for input
        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONDOWN:  # mouse click coordinates
            x, y = event.pos
            w = settings.screen_settings.width
            h = settings.screen_settings.height
            if 0 < x < w and 0 < y < h:
                self.active_event = 'moving'
                self.click_coordinates = (x, y)
        elif event.type == pygame.MOUSEMOTION:
            self.input = 'mouse motion'
            self.hover_coordinates = event.pos
        elif event.type == pgl.QUIT:
            self.active_event = 'quit'
        elif event.type == pgl.KEYDOWN:  # pressed keyboard key
            # find out the active event from keyboard commands dictionary
            keyboard = self.game.current_state.ID
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
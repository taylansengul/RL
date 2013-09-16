import pygame.locals as pgl
from globals import *
import settings
import pygame


class IO(object):
    previous_event = None
    active_event = None
    click_coordinates = (-1, -1)
    hover_coordinates = (-1, -1)
    keyboard_commands_dictionary = {
        MAP_STATE: {
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
        MAIN_MENU_STATE: {
            pgl.K_DOWN: 'down',
            pgl.K_UP: 'up',
            pgl.K_RETURN: 'select'},
        GAME_OVER_STATE: {
            pgl.K_SPACE: 'pass'},
        INVENTORY_STATE: {
            pgl.K_DOWN: 'down',
            pgl.K_UP: 'up',
            pgl.K_RETURN: 'select',
            pgl.K_ESCAPE: 'quit',
            pgl.K_e: 'show edible items',
            pgl.K_u: 'show consumable items'},
        TARGETING_STATE: {
            pgl.K_RIGHT: 'right',
            pgl.K_LEFT: 'left',
            pgl.K_DOWN: 'down',
            pgl.K_UP: 'up',
            pgl.K_RETURN: 'select'}}

    @staticmethod
    def compute_active_event(current_state_ID):
        """compute the active event"""
        # reset variables
        IO.previous_event = IO.active_event  # previous event = previous active event
        IO.click_coordinates = (-1, -1)
        IO.hover_coordinates = (-1, -1)
        # wait for input
        if IO.active_event == 'pass':
            IO.active_event = None
            return
        IO.active_event = None
        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONDOWN:  # mouse click coordinates
            x, y = event.pos
            w = settings.screen_settings.width
            h = settings.screen_settings.height
            if 0 < x < w and 0 < y < h:
                IO.active_event = 'moving'
                IO.click_coordinates = (x, y)
        elif event.type == pygame.MOUSEMOTION:
            IO.input = 'mouse motion'
            IO.hover_coordinates = event.pos
        elif event.type == pgl.QUIT:
            IO.active_event = 'quit'
        elif event.type == pgl.KEYDOWN:  # pressed keyboard key
            # find out the active event from keyboard commands dictionary
            keyboard = current_state_ID
            for key in IO.keyboard_commands_dictionary[keyboard]:
                if event.key == key:
                    IO.active_event = IO.keyboard_commands_dictionary[keyboard][key]

    @staticmethod
    def get_active_event():
        return IO.active_event

    @staticmethod
    def get_click_coordinates():
        return IO.click_coordinates

    @staticmethod
    def get_hover_coordinates():
        return IO.hover_coordinates

    @staticmethod
    def set_active_event(event):
        IO.active_event = event
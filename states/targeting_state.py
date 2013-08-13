import pygame as pg
import data


class Inventory_State(object):
    def __init__(self, game):
        self.ID = 'targeting state'
        self.game = game
        self.selected_tile = None
        self.highlighted_tile = self.game.objects_handler.player.tile

    def init(self):
        pass

    def updateScreen(self):
        self.game.state_manager.map_state.updateScreen()

    def determineAction(self):
        event = self.game.io_handler.get_active_event()
        if event == 'down':
            self.menu.select_next()
        elif event == 'up':
            self.menu.select_prev()
        elif event == 'select':
            option = self.menu.get_active_option()
        elif event == 'quit':
            self.game.state_manager.change_state(self.game.state_manager.map_state)
import data
import pygame as pg


class Game_Over_State(object):
    def __init__(self, game):
        self.game = game
        self.name = 'game over state'

    def init(self):
        pass

    def determineAction(self):
        event = self.game.io_handler.get_active_event()
        if event == 'pass':
            self.game.state_manager.change_state(self.game.state_manager.main_menu_state)

    def updateScreen(self):
        graphics = self.game.graphics_engine
        graphics.screens['main'].fill(data.Colors.palette['black'])
        graphics.fontMgr.Draw(graphics.screens['main'], 'arial', 36, 'Game is over.',
            (0, 0), data.Colors.palette['white'], 'center', 'center', True)
        graphics.fontMgr.Draw(graphics.screens['main'], 'arial', 36, self.game.logger.game_over_message,
            (0, 40), data.Colors.palette['white'], 'center', 'center', True)
        graphics.fontMgr.Draw(graphics.screens['main'], 'arial', 36, 'Press Space.',
            (0, 80), data.Colors.palette['white'], 'center', 'center', True)
        pg.display.flip()
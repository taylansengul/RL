from globals import *
from systems.draw import Draw
from systems.IO import IO


class Game_Over_Screen_State(object):
    def __init__(self, game):
        self.game = game
        self.ID = GAME_OVER_STATE
        self.screens = {GAME_OVER_SCREEN: None}

    def init(self):
        self.updateScreen()

    def determineAction(self):
        event = IO.active_event
        if event == 'pass':
            self.game.change_state(self.game.main_menu_state)

    def updateScreen(self):
        screen = self.screens[GAME_OVER_SCREEN]
        Draw.game_over_messages(screen)
from globals import *
from systems import draw
from systems.IO import IO


class Game_Over_Screen_State(object):
    def __init__(self, game):
        self.game = game
        self.ID = GAME_OVER_STATE

    def init(self):
        self.updateScreen()

    def determineAction(self):
        event = IO.active_event
        if event == 'pass':
            self.game.change_state(self.game.main_menu_state)

    def updateScreen(self):
        draw.game_over_messages()
from globals import *
from map_state_screen_updater import MapStateScreenUpdater
from map_state_logic_engine import MapStateLogicEngine


class Map_State(object):
    def __init__(self, game):
        self.game = game
        self.ID = MAP_STATE
        self.logic_engine = MapStateLogicEngine(game)

    def init(self):
        self.updateScreen()

    def determineAction(self):
        self.logic_engine.run()

    def updateScreen(self):
        MapStateScreenUpdater.run()
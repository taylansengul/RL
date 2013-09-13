from globals import *
from map_state_screen_updater import MapStateScreenUpdater
from map_state_logic_engine import MapStateLogicEngine


class Map_State(object):
    def __init__(self, game):
        self.game = game
        self.ID = MAP_STATE
        self.screens = {
            MAP_SCREEN: None,
            PLAYER_SCREEN: None,
            GAME_INFO_SCREEN: None,
            MESSAGES_SCREEN: None,
            ENEMY_SCREEN: None}
        self.images = {}
        self.screen_updater = MapStateScreenUpdater(game, self.screens)
        self.logic_engine = MapStateLogicEngine(game)

    def init(self):
        self.updateScreen()

    def determineAction(self):
        self.logic_engine.run()

    def updateScreen(self):
        self.screen_updater.run()

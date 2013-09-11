import os
import globals as g
from map_state_screen_updater import MapStateScreenUpdater
from map_state_logic_engine import MapStateLogicEngine


class Map_State(object):
    def __init__(self, game):
        self.game = game
        self.ID = g.states.MAP
        self.screens = {'map': None, 'player': None, 'game info': None, 'messages': None, 'enemy': None}
        self.images = {}
        self.screen_updater = MapStateScreenUpdater(game, self.screens)
        self.logic_engine = MapStateLogicEngine(game)

    def init(self):
        image_location = os.path.join('images', "floor_tile.png")
        self.images['floor'] = self.game.pygame.image.load(image_location).convert_alpha()
        self.updateScreen()

    def determineAction(self):
        self.logic_engine.run()

    def updateScreen(self):
        self.screen_updater.run()

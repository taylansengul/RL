from globals import *
from entities.entity import Entity
from systems.IO import IO
from systems import draw
from entities.game_world import Game_World


class Targeting_State(object):
    def __init__(self, game):
        self.ID = TARGETING_STATE
        self.game = game
        self.selected_tile = None
        self.highlighted_tile = None

    def init(self):
        self.selected_tile = None
        self.highlighted_tile = Entity.player.tile

    def determineAction(self):
        event = IO.active_event
        if event in ['left', 'right', 'up', 'down']:
            self.highlighted_tile = Game_World.dungeon.get_neighbor_tile(self.highlighted_tile, event)
        elif event == 'select':
            self.selected_tile = self.highlighted_tile
            self.game.change_state(MAP_STATE)

    def updateScreen(self):
        self.game.map_state.updateScreen()
        coordinates = self.highlighted_tile.screen_position
        draw.highlighted_tile_border(coordinates)
        draw.update()
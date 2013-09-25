import globals
from entities.entity import Entity
from systems import draw
from entities.game_world import Game_World
import base_state


class Targeting_State(base_state.BaseState):
    def __init__(self, game):
        super(Targeting_State, self).__init__(globals.TARGETING_STATE)
        self.game = game
        self.selected_tile = None
        self.highlighted_tile = None

    def init(self):
        self.current_state = self.ID
        self.selected_tile = None
        self.highlighted_tile = Entity.player.tile

    def determine_action(self):
        super(Targeting_State, self).determine_action()
        event = self.get_event()
        dungeon = Game_World.dungeon
        if event in ['left', 'right', 'up', 'down']:
            tile = dungeon.get_neighbor_tile(self.highlighted_tile, event)
            self.highlighted_tile = tile
        elif event == 'select':
            self.selected_tile = self.highlighted_tile
            self.next_game_state = globals.MAP_STATE

    def update_screen(self):
        self.game.map_state.updateScreen()
        coordinates = self.highlighted_tile.screen_position
        draw.highlighted_tile_border(coordinates)
        draw.update()

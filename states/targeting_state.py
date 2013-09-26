import base_state
from entities.entity import Entity
from entities.game_world import Game_World
import enums
from systems import draw


class TargetingState(base_state.BaseState):
    def __init__(self):
        super(TargetingState, self).__init__(enums.TARGETING_STATE)
        self.selected_tile = None
        self.highlighted_tile = None
        self.current_state = None

    def init(self):
        super(TargetingState, self).init()
        self.current_state = self.ID
        self.selected_tile = None
        self.highlighted_tile = Entity.player.tile

    def determine_action(self):
        super(TargetingState, self).determine_action()
        event = self.get_event()
        dungeon = Game_World.dungeon
        if event in ['left', 'right', 'up', 'down']:
            tile = dungeon.get_neighbor_tile(self.highlighted_tile, event)
            self.highlighted_tile = tile
        elif event == 'select':
            self.selected_tile = self.highlighted_tile
            self.next_game_state = enums.MAP_STATE

    def update_screen(self):
        #todo
        self.game.map_state.updateScreen()
        coordinates = self.highlighted_tile.screen_position
        draw.highlighted_tile_border(coordinates)
        draw.update()

import globals
from map_state_logic_engine import MapStateLogicEngine
import base_state
from entities.entity import Entity
from systems import draw
from systems.time import Time


class Map_State(base_state.BaseState):
    def __init__(self, game):
        super(Map_State, self).__init__(globals.MAP_STATE)
        self.game = game
        self.logic_engine = MapStateLogicEngine(game, self)

    def init(self):
        self.update_screen()

    def determine_action(self):
        super(Map_State, self).determine_action()
        self.logic_engine.run()

    def update_screen(self):
        draw.clear_all_screens()
        draw.dungeon(Entity.player, globals.MAP_SCREEN)
        draw.messages_screen()
        draw.player_stats(Entity.player)
        draw.render_turn(Time.turn, globals.GAME_INFO_SCREEN)
        draw.update()

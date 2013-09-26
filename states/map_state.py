import enums
from map_state_logic_engine import MapStateLogicEngine
import base_state
from entities.entity import Entity
from systems import draw
from systems.time import Time


class MapState(base_state.BaseState):
    def __init__(self):
        super(MapState, self).__init__(enums.MAP_STATE)
        self.logic_engine = MapStateLogicEngine(self)

    def init(self):
        self.update_screen()

    def determine_action(self):
        super(MapState, self).determine_action()
        self.logic_engine.run()

    def update_screen(self):
        draw.clear_all_screens()
        draw.dungeon(Entity.player, enums.MAP_SCREEN)
        draw.messages_screen()
        draw.player_stats(Entity.player)
        draw.render_turn(Time.turn, enums.GAME_INFO_SCREEN)
        draw.update()

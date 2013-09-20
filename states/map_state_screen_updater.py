from globals import *
from entities.entity import Entity
from systems import draw
from systems.time import Time


class MapStateScreenUpdater():
    @staticmethod
    def run():
        draw.clear_all_screens()
        draw.dungeon(Entity.player, MAP_SCREEN)
        draw.messages_screen()
        draw.player_stats(Entity.player)
        draw.render_turn(Time.turn, GAME_INFO_SCREEN)
        draw.update()
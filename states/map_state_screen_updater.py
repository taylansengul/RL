from globals import *
from entities.entity import Entity
from systems import Logger
from systems import draw
from systems.time import Time


class MapStateScreenUpdater():
    def __init__(self, screens):
        self.screens = screens

    def _draw_dungeon(self):
        draw.dungeon(Entity.player, self.screens[MAP_SCREEN])

    def _draw_message_console(self):
        screen = self.screens[MESSAGES_SCREEN]
        Logger.display_messages(screen)

    def _draw_player_stats(self):
        draw.player_stats(Entity.player)

    def _draw_turn_info(self):
        screen = self.screens[GAME_INFO_SCREEN]
        draw.render_turn(Time.turn, screen)

    def _clear_all_screens(self):
        for ID in self.screens:
            self.screens[ID].clear()

    def run(self):
        self._clear_all_screens()
        self._draw_dungeon()
        self._draw_message_console()
        self._draw_player_stats()
        self._draw_turn_info()
        draw.update()
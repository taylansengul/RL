from globals import *
from objects.entity import Entity


class MapStateScreenUpdater():
    def __init__(self, game, screens):
        self.game = game
        self.screens = screens

    def _draw_dungeon(self):
        self.game.game_world.dungeon.draw(self.screens[MAP_SCREEN])

    def _draw_message_console(self):
        self.game.logger.display_messages()

    def _draw_player_stats(self):
        Entity.player.render_stats()

    def _draw_turn_info(self):
        self.game.time.render_turn()

    def _clear_all_screens(self):
        for ID in self.screens:
            self.screens[ID].clear()

    def run(self):
        self._clear_all_screens()
        self._draw_dungeon()
        self._draw_message_console()
        self._draw_player_stats()
        self._draw_turn_info()
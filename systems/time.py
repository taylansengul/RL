from graphics.text import Text
from globals import *


class Time(object):
    def __init__(self, game):
        self.game = game
        self.turn = 1

    def new_turn(self):
        # update player status
        self.game.objects_handler.player.update_status()
        # player vision changes
        self.game.objects_handler.player.update_vision()
        # ai action
        # do not need ai: self.game.ai.determine_total_action()
        self.turn += 1
        # run resource manager
        self.game.resource_manager.manage()

    def render_turn(self):
        t = Text(screen=self.game.state_manager.map_state.screens[ScreenID.GAME_INFO],
                 context='turn: %d' % self.turn, font=FontID.CONSOLE, coordinates=(0, 0), color='white')
        t.render()
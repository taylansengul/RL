from graphics.text import Text
from globals import *
from entities.entity import Entity
from systems.resource_manager import ResourceManager


class Time(object):
    def __init__(self, game):
        self.game = game
        self.turn = 1

    def new_turn(self):
        # update player status
        Entity.player.update_status()
        # player vision changes
        Entity.player.update_vision()
        # ai action
        # do not need ai: self.game.ai.determine_total_action()
        self.turn += 1
        # run resource manager
        ResourceManager.manage()

    def render_turn(self):
        t = Text(screen=self.game.map_state.screens[GAME_INFO_SCREEN],
                 context='turn: %d' % self.turn, font=CONSOLE_FONT, coordinates=(0, 0), color='white')
        t.render()
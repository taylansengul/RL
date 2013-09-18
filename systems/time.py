from graphics.text import Text
from globals import *
from entities.entity import Entity
from systems import logger
from systems.resource_manager import ResourceManager


class Time(object):
    def __init__(self, game):
        self.game = game
        self.turn = 1

    def new_turn(self):
        # run resource manager
        ResourceManager.manage()

        # update NPC status
        for NPC in Entity.all_NPCs:
            message, __ = NPC.update_status()
            logger.Logger.add_message(message)
        # update player status
        message, game_over = Entity.player.update_status()

        if game_over:
            logger.Logger.game_over_message = message
            self.game.change_state(self.game.game_over_screen_state)

        # player vision changes
        Entity.player.update_vision()
        # todo: ai action
        self.turn += 1

    def render_turn(self):
        t = Text(screen=self.game.map_state.screens[GAME_INFO_SCREEN],
                 context='turn: %d' % self.turn, font=CONSOLE_FONT, coordinates=(0, 0), color='white')
        t.render()
from entities.entity import Entity
from systems.resource_manager import ResourceManager


class Time(object):
    turn = 1

    @staticmethod
    def new_turn():
        messages = []
        # run resource manager
        ResourceManager.manage()
        # update NPC status
        for NPC in Entity.all_NPCs:
            message, __ = NPC.update_status()
            messages.append(message)
        # update player status
        game_over_message, game_over = Entity.player.update_status()

        # player vision changes
        Entity.player.update_vision()
        # todo: ai action
        Time.turn += 1
        return messages, game_over, game_over_message

import random


class AI(object):
    def __init__(self, NPCs):
        self.NPCs = NPCs

    def determine_total_action(self, sys):
        game_world = sys.game_world
        for npc in self.NPCs:
            move_keys = {'move left': (-1, 0), 'move right': (1, 0), 'move up': (0, -1), 'move down': (0, 1)}
            event = random.choice(move_keys.keys())
            npc.move(game_world, sys, event)


import random


class AI(object):
    def __init__(self, game):
        self.game = game
        self.NPCs = game.objects_handler.NPCs

    def determine_total_action(self):
        for npc in self.NPCs:
            # todo: this code is repeated in map_state
            move_keys = {'move left': (-1, 0), 'move right': (1, 0), 'move up': (0, -1), 'move down': (0, 1)}
            event = random.choice(move_keys.keys())
            x, y = npc.coordinates[0] + move_keys[event][0], npc.coordinates[1] + move_keys[event][1]
            target_tile = self.game.game_world.get_tile((x, y))
            if not target_tile or 'movement blocking' in target_tile.properties:  # tile not valid or movement blocking
                self.game.io_handler.set_active_event(None)
            elif self.game.event_log[-2] == 'close door':
                npc.close_door(event)
            elif target_tile.tip == 'closed door':  # target tile = closed door
                npc.open_door()
            else:  # if the target tile is a valid tile.
                npc.move(target_tile)  # move
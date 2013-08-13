import random


class AI(object):
    def __init__(self, game):
        self.game = game
        self.NPCs = game.objects_handler.NPCs

    def determine_total_action(self):
        for npc in self.NPCs:
            # todo: this code is repeated in map_state:
            event = random.choice(['up', 'down', 'left', 'right'])
            target_tile = self.game.game_world.dungeon.get_neighbor_tile(self.tile, event)
            if not target_tile or 'movement blocking' in target_tile.properties:  # tile not valid or movement blocking
                self.game.io_handler.set_active_event(None)
            elif self.game.event_log[-2] == 'close door':
                npc.close_door(event)
            elif target_tile.tip == 'closed door':  # target tile = closed door
                npc.open_door()
            else:  # if the target tile is a valid tile.
                npc.move(target_tile)  # move
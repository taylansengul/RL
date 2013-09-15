from objects.player import Player
from objects.game_entity import Game_Entity
from random import randint
import data


class Objects_Handler():
    def __init__(self, game):
        self.game = game
        self.player = None
        self.NPCs = []
        self.game_items = []
        self.all_objects = []

    def create_player(self):
        m, n = self.game.game_world.dungeon.player_starting_coordinates
        player_tile = self.game.game_world.dungeon.map2D[m][n]
        player = Player(self.game, key='fighter', tile=player_tile)
        self.player = player
        player_tile.container.add(player)
        player.update_vision()

    def populate_game_items(self):
        print 'populating game items...',
        for item in data.level_design.game_items:
            number_of_objects = randint(item['number'][0], item['number'][1])
            for _ in range(number_of_objects):
                tile = self.game.game_world.dungeon.get_random_room_floor_tile_with_no_objects()
                kwargs = data.game_items.dictionary[item['id']]
                new_item = Game_Entity(self.game, tile=tile, **kwargs)
                self.add_game_item(new_item, tile)
        print 'done.'

    def populate_NPCs(self):
        print 'populating NPCs...',
        for item in data.level_design.NPCs:
            number_of_objects = randint(item['number'][0], item['number'][1])
            for _ in range(number_of_objects):
                tile = self.game.game_world.dungeon.get_random_room_floor_tile_with_no_objects()
                kwargs = data.NPC.dictionary[item['id']]
                new_NPC = Game_Entity(self.game, tile=tile, **kwargs)
                self.add_NPC(new_NPC, tile)
        print 'done.'

    def add_NPC(self, NPC, game_object):
        self.NPCs.append(NPC)
        self.all_objects.append(NPC)
        game_object.container.add(NPC)

    def remove_NPC(self, NPC, game_object):
        self.NPCs.remove(NPC)
        self.all_objects.remove(NPC)
        game_object.container.remove(NPC)

    def add_game_item(self, item, game_object):
        self.game_items.append(item)
        self.all_objects.append(item)
        game_object.container.append(item)

    def remove_game_item(self, item, game_object):
        self.game_items.remove(item)
        self.all_objects.remove(item)
        game_object.container.remove(item)
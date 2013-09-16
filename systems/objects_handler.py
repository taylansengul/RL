from objects.player import Player
from objects.entity import Entity
from random import randint
import data


class Objects_Handler():
    def __init__(self, game):
        self.game = game

    def create_player(self):
        m, n = self.game.game_world.dungeon.player_starting_coordinates
        player_tile = self.game.game_world.dungeon.map2D[m][n]
        key = 'fighter'
        kwargs = data.classes.dictionary[key]
        kwargs.update(data.classes.player_settings)
        kwargs['tile'] = player_tile
        player = Player(self.game, **kwargs)
        player_tile.container.add(player)
        player.update_vision()

    def populate_game_items(self):
        print 'populating game items...',
        for item in data.level_design.game_items:
            number_of_objects = randint(item['number'][0], item['number'][1])
            for _ in range(number_of_objects):
                tile = self.game.game_world.dungeon.get_random_room_floor_tile_with_no_objects()
                kwargs = data.game_items.dictionary[item['id']]
                new_item = Entity(self.game, tile=tile, **kwargs)
                tile.container.append(new_item)
        print 'done.'

    def populate_NPCs(self):
        print 'populating NPCs...',
        for item in data.level_design.NPCs:
            number_of_objects = randint(item['number'][0], item['number'][1])
            for _ in range(number_of_objects):
                tile = self.game.game_world.dungeon.get_random_room_floor_tile_with_no_objects()
                kwargs = data.NPC.dictionary[item['id']]
                new_NPC = Entity(self.game, tile=tile, **kwargs)
                tile.container.add(new_NPC)
        print 'done.'

from entities.entity import Entity
from random import randint
import data
from entities.game_world import Game_World
from systems.debuger import debuger


class ObjectsHandler():
    @staticmethod
    def create_player():
        m, n = Game_World.dungeon.player_starting_coordinates
        debuger.info("player coordinates: m=%d, n=%d" % (m, n))
        player_tile = Game_World.dungeon.map2D[m][n]
        key = 'fighter'
        kwargs = data.classes.dictionary[key]
        kwargs.update(data.classes.player_settings)
        kwargs['tile'] = player_tile
        player = Entity(**kwargs)
        for ID in kwargs.get('inventory', None):  # creating self.container from string list
            item_kwargs = data.game_items.dictionary[ID]
            new_item = Entity(tile=player.tile, **item_kwargs)
            player.container.add(new_item)
        player_tile.container.add(player)
        player.update_vision()

    @staticmethod
    def populate_game_items():
        debuger.info('populating game items...')
        for item in data.level_design.game_items:
            number_of_objects = randint(item['number'][0], item['number'][1])
            for _ in range(number_of_objects):
                tile = Game_World.dungeon.get_random_room_floor_tile_with_no_objects()
                kwargs = data.game_items.dictionary[item['id']]
                new_item = Entity(tile=tile, **kwargs)
                tile.container.append(new_item)
        debuger.info('done.')

    @staticmethod
    def populate_NPCs():
        debuger.info('populating NPCs...')
        for item in data.level_design.NPCs:
            number_of_objects = randint(item['number'][0], item['number'][1])
            for _ in range(number_of_objects):
                tile = Game_World.dungeon.get_random_room_floor_tile_with_no_objects()
                kwargs = data.NPC.dictionary[item['id']]
                new_NPC = Entity(tile=tile, **kwargs)
                tile.container.add(new_NPC)
        debuger.info('done.')
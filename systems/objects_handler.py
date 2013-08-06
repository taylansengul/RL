from objects.player import Player
from objects.basic_object import Game_Object
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
        starting_coordinates = self.game.game_world.dungeon.player_starting_coordinates
        player_tile = self.game.game_world.get_tile(starting_coordinates)
        player = Player(self.game, key='fighter', tile=player_tile)
        self.player = player
        self.game.game_world.get_tile(starting_coordinates).add_object(player)
        player.update_vision()

    def populate_game_items(self):
        print 'populating game items'
        item_list = data.level_design.game_items
        for item in item_list:
            ID = item['item']
            number_of_items = randint(item['number'][0], item['number'][1])
            kwargs = dict(data.game_items.dictionary[ID].items() + item.items())
            for _ in range(number_of_items):
                while True:
                    coordinates = self.game.game_world.dungeon.get_random_room_floor()
                    tile = self.game.game_world.get_tile(coordinates)
                    if not tile.has_objects():
                        break
                new_item = Game_Object(self.game, tile=tile, **kwargs)
                self.add_game_item(new_item, tile)

    def create_player_items(self):
        print 'creating player items'
        inventory = data.classes.dictionary[self.game.objects_handler.player.player_class]['objects']
        for item in inventory:
            kwargs = dict(data.game_items.dictionary[item].items())
            new_item = Game_Object(self.game, tile=self.player.tile, **kwargs)
            self.add_game_item(new_item, self.player)

    def populate_NPCs(self):
        print 'populating NPCs'
        NPC_list = data.level_design.NPCs
        for creature in NPC_list:
            number_of_creatures = randint(creature['number'][0], creature['number'][1])
            for _ in range(number_of_creatures):
                while True:
                    coordinates = self.game.game_world.dungeon.get_random_room_floor()
                    tile = self.game.game_world.get_tile(coordinates)
                    if not tile.has_objects():
                        break
                kwargs = data.NPC.dictionary[creature['race']]
                new_NPC = Game_Object(self.game, tile=tile, **kwargs)
                self.add_NPC(new_NPC, tile)

    def add_NPC(self, NPC, game_object):
        self.NPCs.append(NPC)
        self.all_objects.append(NPC)
        game_object.add_object(NPC)

    def remove_NPC(self, NPC, game_object):
        self.NPCs.remove(NPC)
        self.all_objects.remove(NPC)
        game_object.remove_object(NPC)

    def add_game_item(self, item, game_object):
        self.game_items.append(item)
        self.all_objects.append(item)
        game_object.objects.append(item)

    def remove_game_item(self, item, game_object):
        self.game_items.remove(item)
        self.all_objects.remove(item)
        game_object.objects.remove(item)


def main():
    o = Objects_Handler()

if __name__ == '__main__':
    main()
from objects.player import Player
from objects.basic_object import Game_Object
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
        player = Player(self.game, key='fighter', coordinates=starting_coordinates)
        self.player = player
        self.game.game_world.get_tile(starting_coordinates).add_object(player)
        player.update_vision()

    def populate_game_items(self):
        item_list = data.Level_Design.game_items
        for item in item_list:
            name = item['item']
            kwargs = dict(data.game_items.dictionary[name].items() + item.items())
            for _ in range(item['total']):
                kwargs['coordinates'] = self.game.game_world.dungeon.get_random_room_floor()
                new_item = Game_Object(self.game, **kwargs)
                tile = self.game.game_world.get_tile(kwargs['coordinates'])
                self.add_game_item(new_item, tile)

    def populate_NPCs(self):
        NPC_list = data.Level_Design.NPCs
        for _ in range(0, 20):
            for NPC in NPC_list:
                coordinates = self.game.game_world.dungeon.get_random_room_floor()
                race = data.NPCs.dict_[NPC['item']]
                new_NPC = Game_Object(self.game, coordinates=coordinates, **race)
                self.NPCs.append(new_NPC)
                tile = self.game.game_world.get_tile(coordinates)
                self.add_game_item(new_NPC, tile)

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
        game_object.add_object(item)

    def remove_game_item(self, item, game_object):
        self.game_items.remove(item)
        self.all_objects.remove(item)
        game_object.remove_object(item)


def main():
    o = Objects_Handler()

if __name__ == '__main__':
    main()
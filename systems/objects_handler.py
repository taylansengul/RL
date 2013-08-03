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
        player.vision_update()

    def populate_game_items(self):
        item_list = data.Level_Design.game_items
        for item in item_list:
            name = item['item']
            kwargs = dict(data.game_items.dictionary[name].items() + item.items())
            for _ in range(item['total']):
                kwargs['coordinates'] = self.game.game_world.dungeon.get_random_room_floor()
                new_item = Game_Object(self.game, **kwargs)
                tile = self.game.game_world.get_tile(kwargs['coordinates'])
                tile.add_object(new_item)

    def populate_NPCs(self):
        NPC_list = data.Level_Design.NPCs
        for _ in range(0, 20):
            for NPC in NPC_list:
                coordinates = self.game.game_world.dungeon.get_random_room_floor()
                race = data.NPCs.dict_[NPC['item']]

                NPC = Game_Object(self.game, coordinates=coordinates, **race)
                self.NPCs.append(NPC)
                tile = self.game.game_world.get_tile(coordinates)
                tile.add_object(NPC)

    def remove_NPC(self, NPC):
        self.NPCs.remove(NPC)
        self.all_objects.remove(NPC)

    def remove_game_item(self, item_):
        self.game_items.remove(item_)
        self.all_objects.remove(item_)


def main():
    o = Objects_Handler()

if __name__ == '__main__':
    main()
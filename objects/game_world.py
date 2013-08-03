from systems.objects_handler import Objects_Handler
import data
from objects.humanoid import Humanoid
from objects.consumable_object import Consumable_Object
from objects.player import Player
from dungeon import Dungeon


class Game_World(object):
    player_starting_coordinates = (1, 1)

    def __init__(self):
        kwargs = data.Level_Design.dungeon_level_1
        self.dungeon = Dungeon(**kwargs)
        self.tiles_list = []
        for m in range(kwargs['dungeon width']):
            for n in range(kwargs['dungeon height']):
                self.tiles_list.append(self.dungeon.map2D[m][n])

        neighbors_of_starting_tile = self.get_neighbors(self.get_tile(Game_World.player_starting_coordinates), 2)
        # 2 = player.visibility radius
        for t in neighbors_of_starting_tile:
            t.isVisible = True
            t.explored = True

        # objects
        self.objects = Objects_Handler()
        self.create_level_items()
        self.create_NPCs()
        self.create_player()

    def change_position_of(self, object_, new_coordinates):
        old_tile = self.get_tile(object_.coordinates)
        new_tile = self.get_tile(new_coordinates)
        old_tile.remove_object(object_)
        new_tile.add_object(object_)
        # change object coordinates
        object_.coordinates = new_coordinates

    def create_player(self):
        starting_coordinates = self.dungeon.player_starting_coordinates
        player = Player('fighter', coordinates=starting_coordinates)
        self.objects.add_player(player)
        self.get_tile(starting_coordinates).add_object(player)

    def create_item(self, **kwargs):
        if kwargs['type'] == 'consumable':
            item_ = Consumable_Object(**kwargs)
            self.objects.add_game_item(item_)
            self.get_tile(kwargs['coordinates']).add_object(item_)

    def create_level_items(self):
        item_list = data.Level_Design.game_items
        for item in item_list:
            name = item['item']
            kwargs = dict(data.Items.dict_[name].items() + item.items())
            self.create_item(**kwargs)

    def create_NPCs(self):
        NPC_list = data.Level_Design.NPCs
        for NPC in NPC_list:
            coordinates = NPC['coordinates']
            race = data.NPCs.dict_[NPC['item']]
            NPC = Humanoid(coordinates=coordinates, **race)
            self.objects.add_NPC(NPC)
            self.get_tile(coordinates).add_object(NPC)

    def get_tile(self, coordinates):
        w, h = self.dungeon.dungeon_width, self.dungeon.dungeon_height
        x, y = coordinates
        if 0 <= x <= w and 0 <= y <= h:
            return self.dungeon.map2D[x][y]
        else:
            return False

    def get_neighbors(self, tile, radius):
        neighbors = []
        x, y = tile.coordinates
        for m in range(max(x - radius, 0), min(x + radius, self.dungeon.dungeon_width)):
            for n in range(max(y - radius, 0), min(y + radius, self.dungeon.dungeon_height)):
                neighbors.append(self.dungeon.map2D[m][n])
        return neighbors
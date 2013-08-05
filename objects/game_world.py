import data

from dungeon import Dungeon


class Game_World(object):
    def __init__(self, game):
        self.game = game
        self.dungeon = None
        self.tiles_list = []

    def set_current_dungeon(self):
        kwargs = data.level_design.dungeon_level_1
        self.dungeon = Dungeon(self.game, **kwargs)
        self.dungeon.create_map()
        for m in range(self.dungeon.dungeon_width):
            for n in range(self.dungeon.dungeon_height):
                self.tiles_list.append(self.dungeon.map2D[m][n])

    def change_position_of(self, object_, new_coordinates):
        old_tile = self.get_tile(object_.coordinates)
        new_tile = self.get_tile(new_coordinates)
        old_tile.remove_object(object_)
        new_tile.add_object(object_)
        # change object coordinates
        object_.coordinates = new_coordinates

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
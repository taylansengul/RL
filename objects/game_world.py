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

    def get_neighbors(self, tile, radius):
        neighbors = []
        x, y = tile.coordinates
        for m in range(max(x - radius, 0), min(x + radius, self.dungeon.dungeon_width)):
            for n in range(max(y - radius, 0), min(y + radius, self.dungeon.dungeon_height)):
                neighbors.append(self.dungeon.map2D[m][n])
        return neighbors
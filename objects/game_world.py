from dungeon import Dungeon
import data


class Game_World(object):
    def __init__(self, game):
        self.game = game
        self.dungeon = None

    def set_current_dungeon(self):
        kwargs = data.level_design.dungeon_level_1
        self.dungeon = Dungeon(self.game, **kwargs)
        self.dungeon.create_map()
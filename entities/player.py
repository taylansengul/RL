from entity import Entity
from systems.utils import get_line
from entities.game_world import Game_World


class Player(Entity):
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)

    @property
    def tiles_in_visibility_radius(self):
        """returns tiles in visibility radius"""
        return Game_World.dungeon.get_neighboring_tiles(self.tile, self.visibility_radius)

    @property
    def visible_tiles(self):
        """returns tiles that are currently visible"""
        return [tile for tile in self.tiles_in_visibility_radius if tile not in self.non_visible_tiles]

    @property
    def non_visible_tiles(self):
        """returns tiles that are not currently visible"""
        dungeon = Game_World.dungeon
        player_x, player_y = self.tile.coordinates
        non_visible_tiles = []
        for tile1 in self.tiles_in_visibility_radius:
            x1, y1 = tile1.coordinates
            vision_ray_coordinates = get_line(player_x, player_y, x1, y1)
            vision_ray_tiles = dungeon.get_tiles(*vision_ray_coordinates)
            for j, tile2 in enumerate(vision_ray_tiles):  # look at the tiles(tile2) on the ray from the player to tile1
                if 'light blocking' in tile2.properties:  # if there is a tile2 which is light blocking
                    for tile3 in vision_ray_tiles[j+1:]:  # all tiles(tile3) after tile2
                        non_visible_tiles.append(tile3)   # are appended to non_visible_tiles list
                    break
        return non_visible_tiles

    def update_vision(self):
        # todo: optimize later (takes 1/1000~2/1000 secs)
        dungeon = Game_World.dungeon
        dungeon.set_all_tiles_non_visible()
        for tile in self.visible_tiles:
            tile.set_visibility(True)

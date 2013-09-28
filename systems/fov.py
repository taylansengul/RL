from entities.game_world import Game_World
from systems import utils


class FOV(object):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    @property
    def tiles_in_visibility_radius(self):
        """returns tiles in visibility radius"""
        return Game_World.dungeon.get_neighboring_tiles(self.center, self.radius)

    @property
    def visible_tiles(self):
        """returns tiles that are currently visible"""
        a = self.tiles_in_visibility_radius
        b = self.non_visible_tiles
        return [tile for tile in a if tile not in b]

    @property
    def non_visible_tiles(self):
        """returns tiles that are not currently visible"""
        dungeon = Game_World.dungeon
        center_x, center_y = self.center.coordinates
        tiles = []
        for tile1 in self.tiles_in_visibility_radius:
            x1, y1 = tile1.coordinates
            vision_ray_coordinates = utils.get_line(center_x, center_y, x1, y1)
            vision_ray_tiles = dungeon.get_tiles(*vision_ray_coordinates)
            for j, tile2 in enumerate(vision_ray_tiles):  # look at the tiles(tile2) on the ray from the player to tile1
                if 'light blocking' in tile2.properties:  # if there is a tile2 which is light blocking
                    for tile3 in vision_ray_tiles[j+1:]:  # all tiles(tile3) after tile2
                        tiles.append(tile3)               # are appended to tiles list
                    break
        return tiles

    def update(self, tile, radius):
        # todo: optimize later (takes 1/1000~2/1000 secs)
        self.center = tile
        self.radius = radius
        Game_World.dungeon.set_all_tiles_non_visible()
        for tile in self.visible_tiles:
            tile.set_visibility(True)
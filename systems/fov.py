__author__ = 'Taylan Sengul'
from systems.utils import get_line


class FOV:
    @staticmethod
    def tiles_in_visibility_radius(tile, radius):
        """returns tiles in visibility radius"""
        return Game_World.dungeon.get_neighboring_tiles(tile, radius)

    @staticmethod
    def visible_tiles(tile, radius):
        """returns tiles that are currently visible"""
        return [tile for tile in FOV.tiles_in_visibility_radius(tile, radius) if tile not in FOV.non_visible_tiles(tile)]

    @staticmethod
    def non_visible_tiles(tile):
        """returns tiles that are not currently visible"""
        player_x, player_y = tile.coordinates
        non_visible_tiles = []
        for tile1 in FOV.tiles_in_visibility_radius:
            x1, y1 = tile1.coordinates
            vision_ray_coordinates = get_line(player_x, player_y, x1, y1)
            vision_ray_tiles = dungeon.get_tiles(*vision_ray_coordinates)
            for j, tile2 in enumerate(vision_ray_tiles):  # look at the tiles(tile2) on the ray from the player to tile1
                if 'light blocking' in tile2.properties:  # if there is a tile2 which is light blocking
                    for tile3 in vision_ray_tiles[j+1:]:  # all tiles(tile3) after tile2
                        non_visible_tiles.append(tile3)   # are appended to non_visible_tiles list
                    break
        return non_visible_tiles

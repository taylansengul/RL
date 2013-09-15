from entity import Entity
from systems.utils import get_line
from graphics.text import Text
from globals import *
import data


class Player(Entity):
    def __init__(self, game, key='Fighter', tile=None):
        kwargs = dict(data.classes.dictionary[key].items())
        kwargs['icon'] = '@'
        kwargs['tile'] = tile
        kwargs['color'] = 'red'
        kwargs['ID'] = 'player'
        super(Player, self).__init__(game, **kwargs)
        self.player_class = key
        self.name = 'George'

    @property
    def tiles_in_visibility_radius(self):
        """returns tiles in visibility radius"""
        return self.game.game_world.dungeon.get_neighboring_tiles(self.tile, self.visibility_radius)

    @property
    def visible_tiles(self):
        """returns tiles that are currently visible"""
        return [tile for tile in self.tiles_in_visibility_radius if tile not in self.non_visible_tiles]

    @property
    def non_visible_tiles(self):
        """returns tiles that are not currently visible"""
        dungeon = self.game.game_world.dungeon
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
        dungeon = self.game.game_world.dungeon
        dungeon.set_all_tiles_non_visible()
        for tile in self.visible_tiles:
            tile.set_visibility(True)

    def close_door(self, target_tile):
        if target_tile.tip != 'open door':
            return
        else:
            target_tile.set_tip('closed door')
            self.game.logger.add_message('Door closed.')

    def update_status(self):
        # player hunger changes
        super(Player, self).update_status()
        if self.hunger.is_zero():
            self.is_alive = False
            self.game.logger.game_over_message = 'You died of hunger.'
        # player vision changes
        Entity.player.update_vision()

        if not self.is_alive:  # player dead
            self.game.change_state(self.game.game_over_screen_state)

    def render_stats(self):
        line_height = 16
        contexts = [self.name,
                    'hp: %d/%d' % (self.hp.current, self.hp.maximum),
                    'hunger: %d/%d' % (self.hunger.current, self.hunger.maximum),
                    'money: %d' % self.money]
        l = len(contexts)
        screens = [self.game.map_state.screens[PLAYER_SCREEN]]*l
        coordinates = [(0, j*line_height) for j in range(l)]
        colors = ['white']*l
        for _ in zip(screens, contexts, coordinates, colors):
            t = Text(font=CONSOLE_FONT, screen=_[0], context=_[1], coordinates=_[2], color=_[3])
            t.render()
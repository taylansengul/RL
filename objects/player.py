from game_object import Game_Object
from systems.utils import get_line
from graphics.text import Text
import globals as g


class Player(Game_Object):
    def __init__(self, game, key='Fighter', tile=None):
        kwargs = dict(game.data.classes.dictionary[key].items())
        kwargs['icon'] = '@'
        kwargs['tile'] = tile
        kwargs['color'] = 'red'
        kwargs['ID'] = 'player'
        super(Player, self).__init__(game, **kwargs)
        self.player_class = key
        self.name = 'Numan'

    @property
    def coordinates_of_tiles_in_visibility_radius(self, radius=5):
        return self.game.game_world.dungeon.get_neighboring_coordinates(self.tile.coordinates,
                                                                          self.visibility_radius)

    @property
    def tiles_in_visibility_radius(self, radius=5):
        return self.game.game_world.dungeon.get_neighboring_tiles(self.tile, self.visibility_radius)

    def update_vision(self):
        # todo: optimize later (takes 1/1000~2/1000 secs)
        game_world = self.game.game_world
        x, y = self.tile.coordinates

        for m in range(game_world.dungeon.dungeon_width):
            for n in range(game_world.dungeon.dungeon_height):
                game_world.dungeon.map2D[m][n].set_visibility(False)      # make every tile invisible

        non_visible_tiles = []
        for X in self.coordinates_of_tiles_in_visibility_radius:
            x1, y1 = X
            vision_ray_coordinates = get_line(x, y, x1, y1)
            vision_ray_tiles = [game_world.dungeon.map2D[c[0]][c[1]] for c in vision_ray_coordinates]
            line_blocking_status = ['light blocking' in _.properties for _ in vision_ray_tiles]
            for j, b in enumerate(line_blocking_status):
                if b:  # if found a light blocking tile t
                    for each in vision_ray_tiles[j+1:]:  # tiles after that tile
                        non_visible_tiles.append(each)  # are appended to non_visible_tiles list
                    break

        for X in self.coordinates_of_tiles_in_visibility_radius:  # go over
            x1, y1 = X
            t = self.game.game_world.dungeon.map2D[x1][y1]
            t.set_visibility(False) if t in non_visible_tiles else t.set_visibility(True)

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
        self.game.objects_handler.player.update_vision()

        if not self.is_alive:  # player dead
            sM = self.game.state_manager
            sM.change_state(sM.game_over_screen_state)

    def render_stats(self):
        line_height = 16
        contexts = [self.name,
                    'hp: %d/%d' % (self.hp.current, self.hp.capacity),
                    'hunger: %d/%d' % (self.hunger.current, self.hunger.capacity),
                    'money: %d' % self.money]
        l = len(contexts)
        screens = [self.game.state_manager.map_state.screens['player']]*l
        coordinates = [(0, j*line_height) for j in range(l)]
        colors = ['white']*l
        for _ in zip(screens, contexts, coordinates, colors):
            t = Text(font=g.FontID.CONSOLE, screen=_[0], context=_[1], coordinates=_[2], color=_[3])
            t.render()
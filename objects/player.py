from data import classes, colors
from basic_object import Game_Object
from systems.utils import get_line


class Player(Game_Object):
    def __init__(self, game, key='Fighter', coordinates=None):
        kwargs = dict(classes.dictionary[key].items())
        kwargs['icon'] = '@'
        kwargs['coordinates'] = coordinates
        kwargs['color'] = 'red'
        kwargs['id'] = 'player'
        super(Player, self).__init__(game, **kwargs)
        self.player_class = key
        self.name = 'Numan'

    def update_vision(self):
        # todo: optimize later (takes 1/1000~2/1000 secs)
        game_world = self.game.game_world
        x, y = self.coordinates
        player_tile = game_world.get_tile((x, y))

        for tile in game_world.tiles_list:  # make every tile
            tile.set_visibility(False)      # invisible

        non_visible_tiles = []
        tiles_in_visibility_radius = game_world.get_neighbors(player_tile, self.visibility_radius)
        for tile in tiles_in_visibility_radius:
            x1, y1 = tile.coordinates
            vision_ray_coordinates = get_line(x, y, x1, y1)
            vision_ray_tiles = [game_world.get_tile(_) for _ in vision_ray_coordinates]
            line_blocking_status = ['light blocking' in _.properties for _ in vision_ray_tiles]
            for j, b in enumerate(line_blocking_status):
                if b:  # if found a light blocking tile t
                    for _ in vision_ray_tiles[j+1:]:  # tiles after that tile
                        non_visible_tiles.append(_)  # are appended to non_visible_tiles list
                    break

        for _ in tiles_in_visibility_radius:  # go over
            _.set_visibility(False) if _ in non_visible_tiles else _.set_visibility(True)

    def close_door(self, event):
        move_key = {'move left': (-1, 0), 'move right': (1, 0), 'move up': (0, -1), 'move down': (0, 1)}
        current_x, current_y = self.coordinates
        target_x, target_y = current_x + move_key[event][0], current_y + move_key[event][1]
        target_tile = self.game.game_world.get_tile((target_x, target_y))
        if not target_tile:
            return
        elif target_tile.tip != 'open door':
            return
        else:
            target_tile.set_tip('closed door')
            self.game.logger.add_message('Door closed.')

    def update_status(self):
        # player hunger changes
        super(Player, self).update_status()
        self.hunger.change_current(-1)
        if self.hunger.is_zero():
            self.is_alive = False
            self.game.logger.add_game_over_message = 'You died of hunger.'
        # player vision changes
        self.game.objects_handler.player.update_vision()

        if not self.is_alive:  # player dead
            sM = self.game.state_manager
            sM.change_state(sM.game_over_state)

    def get_display_info(self):
        new_line_height = 16
        st = {'screen': 'player',
              'info': [{'item': self.name,
                        'coordinates': (0, 0),
                        'color': colors.palette['white']},
                       {'item': 'hp: %d/%d' % (self.hp.current, self.hp.capacity),
                        'coordinates': (0, new_line_height),
                        'color': colors.palette['white']},
                       {'item': 'hunger: %d/%d' % (self.hunger.current, self.hunger.capacity),
                        'coordinates': (0, 2*new_line_height),
                        'color': colors.palette['white']},
                       {'item': 'money: %d' % self.money,
                        'coordinates': (0, 3*new_line_height),
                        'color': colors.palette['white']}]}
        return st
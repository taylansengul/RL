from basic_object import Basic_Object
import random


class Movable_Object(Basic_Object):
    def __init__(self, **kwargs):
        super(Movable_Object, self).__init__(**kwargs)
        self.can_open_doors = kwargs['can_open_doors']

    def move(self, game_world, sys, event):
        move_keys = {'move left': (-1, 0), 'move right': (1, 0), 'move up': (0, -1), 'move down': (0, 1)}
        target_x, target_y = self.coordinates[0] + move_keys[event][0], self.coordinates[1] + move_keys[event][1]
        target_tile = game_world.get_tile((target_x, target_y))
        if not target_tile:  # target tile not valid
            return False
        elif target_tile.tip == 'closed door':  # target tile = closed door
            if self.can_open_doors:  # self can open doors
                target_tile.set_tip('open door')
                sys.logger.add_message('Door opened.')
                return True
            else:  # self can not open doors
                return False
        else:  # if the target tile is a valid tile.
            # move
            game_world.change_position_of(self, target_tile.coordinates)
            return True
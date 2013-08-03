from humanoid import Humanoid
from data import Classes
from rechargeable import Rechargeable


class Player(Humanoid):
    def __init__(self, key='Fighter', coordinates=None):
        kwargs = dict(Classes.classes[key].items() + Classes.common_player_properties.items())
        kwargs['icon'] = '@'
        kwargs['coordinates'] = coordinates
        kwargs['color'] = 'blue'
        kwargs['name'] = 'Numan'
        super(Player, self).__init__(**kwargs)
        self.hunger = Rechargeable(capacity=100)
        self.money = 1000
        self.visibility_radius = 2

    def vision_update(self, game_world):
        new_tiles = game_world.get_neighbors(game_world.get_tile(self.coordinates), self.visibility_radius)
        for t in game_world.tiles_list:
            if t in new_tiles:
                t.isVisible = True
            else:
                t.isVisible = False

    def move(self, game_world, sys, event):
        moved = super(Player, self).move(game_world, sys, event)  # moves and returns True/False if move is successful
        if moved:
            self.vision_update(game_world)

    def close_door(self, game_world, sys, event):
        move_key = {'move left': (-1, 0), 'move right': (1, 0), 'move up': (0, -1), 'move down': (0, 1)}
        current_x, current_y = self.coordinates
        target_x, target_y = current_x + move_key[event][0], current_y + move_key[event][1]
        target_tile = game_world.get_tile((target_x, target_y))
        if not target_tile:
            return
        elif target_tile.tip != 'open door':
            return
        else:
            target_tile.set_tip('closed door')
            sys.logger.add_message('Door closed.')

    def make_door(self, game_world):
        tile = game_world.get_tile(self.coordinates)
        tile.set_tip('closed door')

    def update_status(self, sys):
        if self.hunger.is_zero():
            self.is_alive = False
            sys.logger.add_message('You died of hunger.')

    def get_display_info(self):
        from data import Colors
        new_line_height = 16
        st = {'screen': 'player',
              'info': [{'item': self.name,
                        'coordinates': (0, 0),
                        'color': Colors.palette['white']},
                       {'item': 'hp: %d/%d' % (self.hp.current, self.hp.capacity),
                        'coordinates': (0, new_line_height),
                        'color': Colors.palette['white']},
                       {'item': 'hunger: %d/%d' % (self.hunger.current, self.hunger.capacity),
                        'coordinates': (0, 2*new_line_height),
                        'color': Colors.palette['white']},
                       {'item': 'money: %d' % self.money,
                        'coordinates': (0, 3*new_line_height),
                        'color': Colors.palette['white']}]}
        return st
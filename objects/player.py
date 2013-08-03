from data import Classes
from rechargeable import Rechargeable
from basic_object import Game_Object
from systems.utils import get_line


class Player(Game_Object):
    def __init__(self, game, key='Fighter', coordinates=None):
        kwargs = dict(Classes.classes[key].items())
        kwargs['properties'] = Classes.common_player_properties
        kwargs['icon'] = '@'
        kwargs['coordinates'] = coordinates
        kwargs['color'] = 'red'
        kwargs['name'] = 'Numan'
        super(Player, self).__init__(game, **kwargs)
        self.hunger = Rechargeable(capacity=10)
        self.money = 1000
        self.visibility_radius = 6
        self.damage = 3

    def vision_update(self):
        # todo: optimize later (takes 1/1000~2/1000 secs)
        game_world = self.game.game_world
        x, y = self.coordinates
        tiles = game_world.get_neighbors(game_world.get_tile((x, y)), self.visibility_radius)
        for t in game_world.tiles_list:
            t.isVisible = False

        for t in tiles:
            if t.isVisible:
                continue
            x1, y1 = t.coordinates
            line_coordinates = get_line(x, y, x1, y1)
            line_tiles = [game_world.get_tile(c) for c in line_coordinates]
            line_blocking_status = ['blocks light' in t.properties for t in line_tiles]
            for j, b in enumerate(line_blocking_status):
                if b:  # blocks light
                    for t in line_tiles[j+1:]:
                        t.isVisible = False
                    break
                else:
                    t.isVisible = True

    def move(self, event):
        moved = super(Player, self).move(event)  # moves and returns True/False if move is successful
        if moved:
            self.vision_update()

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

    def make_door(self, game_world):
        tile = game_world.get_tile(self.coordinates)
        tile.set_tip('closed door')

    def update_status(self):
        self.game.objects_handler.player.hunger.change_current(-1)
        if self.hunger.is_zero():
            self.is_alive = False
            self.game.logger.add_message('You died of hunger.')

        if not self.is_alive:
            sM = self.game.state_manager
            sM.change_state(sM.main_menu_state)

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
from game_object import Game_Object
import inspect


class Tile(Game_Object):
    # todo: walkable tiles.
    floor_properties = 'container'
    wall_properties = 'movement blocking, light blocking'
    tiles = {'': {'icon': '', 'color': 'white'},
             'wall': {'icon': '#', 'color': 'red', 'properties': wall_properties},
             'entrance': {'icon': '>', 'color': 'yellow', 'properties': floor_properties},
             'exit': {'icon': '<', 'color': 'yellow', 'properties': floor_properties},
             'floor': {'icon': ' ', 'color': 'blue', 'properties': 'container'},
             'open door': {'icon': '-', 'color': 'red'},
             'closed door': {'icon': '+', 'color': 'red'},
             'dirt': {'icon': ' ', 'color': 'black', 'properties': wall_properties}}

    def __init__(self, game, coordinates=None, tip=''):
        kwargs = {'coordinates': coordinates,
                  'icon': Tile.tiles[tip]['icon'],
                  'color': Tile.tiles[tip]['color'],
                  'properties': Tile.tiles[tip].get('properties', ''),
                  'ID': tip}
        super(Tile, self).__init__(game, **kwargs)
        self.coordinates = coordinates
        self.tip = tip
        self.is_explored = False  # tiles which are currently or previously visible . once explored, always explored.
        self.is_visible = False  # tiles which are currently visible. this is set to False every turn.

    def set_tip(self, tip):
        self.tip = tip
        self.icon = Tile.tiles[tip]['icon']
        self.color = Tile.tiles[tip]['color']

    def set_visibility(self, b):
        if b:
            self.is_visible = True
            self.is_explored = True
        else:
            self.is_visible = False
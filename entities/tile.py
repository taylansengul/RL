import pygame
from globals import *
from entity import Entity
import settings


class Tile(Entity):
    # todo: walkable tiles.
    floor_properties = 'tile, drawable, container'
    wall_properties = 'tile, drawable, movement blocking, light blocking'
    tiles = {'': {'icon': '', 'color': 'white'},
             'wall': {'icon': '#', 'color': 'red', 'properties': wall_properties},
             'entrance': {'icon': '>', 'color': 'yellow', 'properties': floor_properties},
             'exit': {'icon': '<', 'color': 'yellow', 'properties': floor_properties},
             'floor': {'icon': ' ', 'color': 'blue', 'properties': floor_properties, 'image': "floor_tile.png"},
             'open door': {'icon': '-', 'color': 'red'},
             'closed door': {'icon': '+', 'color': 'red'},
             'dirt': {'icon': ' ', 'color': 'black', 'properties': wall_properties}}

    def __init__(self, coordinates=None, tip=''):
        kwargs = {'coordinates': coordinates,
                  'icon': Tile.tiles[tip]['icon'],
                  'color': Tile.tiles[tip]['color'],
                  'properties': Tile.tiles[tip].get('properties', None),
                  'image': Tile.tiles[tip].get('image', None),
                  'ID': tip}
        super(Tile, self).__init__(**kwargs)
        self.coordinates = coordinates
        self.tip = tip
        self.is_explored = False  # tiles which are currently or previously visible . once explored, always explored.
        self.is_visible = False   # tiles which are currently visible. this is set to False every turn.

    def set_tip(self, tip):
        self.tip = tip
        self.icon = Tile.tiles[tip]['icon']
        self.color = Tile.tiles[tip]['color']

    def set_visibility(self, a_boolean):
        if a_boolean:
            self.is_visible = True
            self.is_explored = True
        else:
            self.is_visible = False

    @property
    def screen_position(self):
        """returns a pygame.Rect object whose coordinates are normalized w.r.t. player position in the middle"""
        x, y = self.coordinates
        x1, y1 = Entity.player.tile.coordinates
        x2, y2 = settings.screen_settings.map_center_x, settings.screen_settings.map_center_y
        c1 = settings.screen_settings.tile_length * (x - x1 + x2)  # left border coordinate
        c2 = settings.screen_settings.tile_length * (y - y1 + y2)  # top border coordinate
        c3 = settings.screen_settings.tile_length  # length and width
        return pygame.Rect(c1, c2, c3, c3)

    def draw(self, screen):
        self.render_icon_to(screen)

    def draw_tile_objects(self, screen):
        if not 'container' in self.properties:
            return
        for each in self.container:
            each.render_icon_to(screen)

    def draw_tile_border(self, screen):
        pygame.draw.rect(screen, WHITE, self.screen_position, 1)
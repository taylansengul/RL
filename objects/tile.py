import pygame as pg
import globals as g
from game_object import Game_Object


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

    @property
    def screen_position(self):
        """returns a pygame.Rect object whose coordinates are normalized w.r.t. player position in the middle"""
        x, y = self.coordinates
        x1, y1 = self.game.objects_handler.player.tile.coordinates
        x2, y2 = self.game.data.screens.map_center_x, self.game.data.screens.map_center_y
        c1 = self.game.data.screens.tile_length * (x - x1 + x2)  # left border coordinate
        c2 = self.game.data.screens.tile_length * (y - y1 + y2)  # top border coordinate
        c3 = self.game.data.screens.tile_length  # length and width
        return pg.Rect(c1, c2, c3, c3)

    def draw(self, screen):
        if self.tip == 'floor':
            screen.surface.blit(self.game.state_manager.map_state.images['floor'], self.screen_position)
        else:
            self.game.pygame.draw.rect(screen.surface, self.color, self.screen_position)  # tile background
        # self.draw_tile_border(screen)  # uncomment to draw tile border

    def draw_tile_objects(self, screen):
        if not 'container' in self.properties:
            return
        for each in self.objects:
            each.render_icon_to(screen)

    def draw_tile_border(self, screen):
        self.game.pygame.draw.rect(screen, g.colorID.ColorID['white'], self.screen_position, 1)
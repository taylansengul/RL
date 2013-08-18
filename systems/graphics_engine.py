class Graphics_Engine(object):
    def __init__(self, game):
        self.game = game

    def get_screen_position_of(self, (x, y)):
        """returns a pygame.Rect object whose coordinates are normalized w.r.t. player position in the middle"""
        x1, y1 = self.game.objects_handler.player.tile.coordinates
        x2, y2 = self.game.data.screens.map_center_x, self.game.data.screens.map_center_y
        c1 = self.game.data.screens.tile_length * (x - x1 + x2)  # left border coordinate
        c2 = self.game.data.screens.tile_length * (y - y1 + y2)  # top border coordinate
        c3 = self.game.data.screens.tile_length  # length and width
        return self.game.pygame.Rect(c1, c2, c3, c3)
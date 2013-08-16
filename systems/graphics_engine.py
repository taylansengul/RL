import data


class Graphics_Engine(object):
    def __init__(self, game):
        self.game = game
        self.screens = {}
        self.font_manager = None  # is setup in Initializing State

    def init(self):
        self.game.state_manager.current_state.init()

    def get_screen_position_of(self, (x, y)):
        """returns a self.game.pygame.Rect object where coordinates are normalized w.r.t. player position in the middle"""
        x1, y1 = self.game.objects_handler.player.tile.coordinates
        x2, y2 = data.screens.map_center_x, data.screens.map_center_y
        c1 = data.screens.tile_length * (x - x1 + x2)  # left border coordinate
        c2 = data.screens.tile_length * (y - y1 + y2)  # top border coordinate
        c3 = data.screens.tile_length  # length and width
        return self.game.pygame.Rect(c1, c2, c3, c3)

    def display_messages(self):
        new_line_height = 12
        screen = self.screens['messages']
        x, y = data.screens.screen_coordinates[self.game.state_manager.current_state.ID]['messages']
        while self.game.logger.has_unhandled_messages():
            self.game.logger.handle_message()

        self.clear_screen('messages')
        for co, message in enumerate(self.game.logger.message_archive[-4:]):
            self.font_manager.Draw(screen, 'arial', 12, message,
                              self.game.pygame.Rect(0, new_line_height*co, x, y), data.colors.palette['white'], 'left', 'top', True)
        self.screens['main'].blit(screen, (x, y))

    def render_info(self, text_list):
        for text in text_list:
            s_id = text.screen
            screen = self.screens[s_id]
            cs = self.game.state_manager.current_state.ID
            x, y = data.screens.screen_coordinates[cs][s_id]
            r = self.game.pygame.Rect(text.coordinates + (x, y))
            self.font_manager.Draw(screen, 'arial', 12, text.context, r, text.color, 'left', 'top', True)
            self.screens['main'].blit(screen, (x, y))

    def clear_screen(self, screen_name, color='black'):
        if isinstance(color, str):
            color = data.colors.palette[color]
        self.screens[screen_name].fill(color)
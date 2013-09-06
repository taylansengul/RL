from systems.graphics.text import Text


class MessageLogger(object):
    def __init__(self, game):
        self.game = game
        self.message_archive = []
        self.unhandled_messages = []
        self.max_number_of_messages = 4
        self.game_over_message = None

    def add_message(self, message):
        self.unhandled_messages.append(message)

    def has_unhandled_messages(self):
        return len(self.unhandled_messages) > 0

    def handle_message(self):
        message = self.unhandled_messages.pop()
        self.message_archive.append(message)
        return message

    def __str__(self):
        return str(self.message_archive)

    def display_messages(self):
        new_line_height = 12
        screen = self.game.state_manager.map_state.screens['messages']
        x, y = self.game.data.screens.screen_coordinates['map_state']['messages']
        while self.has_unhandled_messages():
            self.handle_message()

        screen.clear()
        for co, message in enumerate(self.game.logger.message_archive[-4:]):
            c = self.game.pygame.Rect(0, new_line_height*co, x, y),
            t = Text(screen=screen, font='console', context=message, coordinates=c, color='white')
            t.render()
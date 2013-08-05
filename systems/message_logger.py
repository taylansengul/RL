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
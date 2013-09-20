#todo: add message with color


class Logger(object):
    message_archive = []
    unhandled_messages = []
    game_over_message = None

    @staticmethod
    def add_message(message):
        """
        add a new message or messages to unhandled_messages.
        :type message: str or list
        """
        if message is None:
            return
        elif isinstance(message, list):
            Logger.unhandled_messages.extend(message)
        elif isinstance(message, str):
            Logger.unhandled_messages.append(message)

    @staticmethod
    def _has_unhandled_messages():
        """
        :return: True if there are unhandled messages, false otherwise.
        """
        return len(Logger.unhandled_messages) > 0

    @staticmethod
    def _handle_message():
        """
        Remove the LAST message from the unhandled_messages and return that message.
        There must be unhandled_messages
        :return: message is a string
        """
        assert Logger._has_unhandled_messages()
        message = Logger.unhandled_messages.pop()
        Logger.message_archive.append(message)
        return message
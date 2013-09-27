#todo: add message with color
def flatten(*args):
    """
    convert args to a single list
    :param args: a variable number of objects/nested lists
    :return: list
    """
    return_list = []

    def recursive_flatten(*inner_args):
        for incoming in inner_args:
            if isinstance(incoming, list):
                for each in incoming:
                    return recursive_flatten(each)
            elif not isinstance(incoming, list) and incoming:
                return_list.append(incoming)

    recursive_flatten(*args)
    return return_list


class Logger(object):
    """
    Used for collecting messages.
    """
    archieve = []
    unhandled_messages = []
    game_over_message = None

    @staticmethod
    def add(*args):
        """
        Add a variable number of messages to Logger.unhandled_messages
        while filtering messages which evalute to false
        (such as '', None, false) under a truth check.
        :param incoming:
        :type incoming: str or list
        """
        flattened_messages = flatten(*args)
        for message in flattened_messages:
            Logger.unhandled_messages.append(message)

    @staticmethod
    def has_unhandled_messages():
        """
        :return: True if there are messages, false otherwise.
        """
        return len(Logger.unhandled_messages) > 0

    @staticmethod
    def handle_message():
        """
        Should only be called if there are unhandled messages.
        Remove the LAST message from the messages, add it to archieve
        and return that message.
        :return: string
        """
        assert Logger.has_unhandled_messages()
        message = Logger.unhandled_messages.pop()
        Logger.archieve.append(message)
        return message
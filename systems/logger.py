#todo: add message with color
from globals import *
from graphics.text import Text
import pygame


class Logger(object):
    message_archive = []
    unhandled_messages = []
    game_over_message = None

    @staticmethod
    def add_message(message):
        """
        add a new message to unhandled_messages.
        :type message: str
        """
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

    @staticmethod
    def display_messages(screen):
        #todo: refactor display_messages
        if not Logger._has_unhandled_messages():
            return
        new_line_height = 12
        x, y = screen.width, screen.height
        while Logger._has_unhandled_messages():
            Logger._handle_message()

        screen.clear()
        for co, message in enumerate(Logger.message_archive[-4:]):
            c = pygame.Rect(0, new_line_height*co, x, y)
            t = Text(screen=screen, font=CONSOLE_FONT, context=message, coordinates=c, color='white')
            t.render()
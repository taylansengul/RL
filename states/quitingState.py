import pygame as pg


class QuitingState(object):
    def __init__(self):
        self.name = 'quiting state'

    def init(self, sys):
        pass

    def updateScreen(self, sys):
        print 'Goodbye'
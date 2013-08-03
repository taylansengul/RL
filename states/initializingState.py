import pygame as pg
import data
from systems.cFontManager import cFontManager


class InitialingState(object):
    def __init__(self):
        self.name = 'initializing state'

    def init(self, sys):
        gE = sys.graphics_engine
        print 'initializing graphics'
        # setup pg
        pg.init()
        # setup main screen
        gE.screens['main'] = pg.display.set_mode(data.Screens.screen_size['main'], 0, 32)
        # Setup the Font
        # avail_fonts = pg.font.get_fonts()
        # avail_fonts = ['arial']
        gE.font_18 = pg.font.SysFont(None, 18)
        gE.font_36 = pg.font.SysFont(None, 36)
        gE.fontMgr = cFontManager((('arial', 12), ('arial', 18), ('arial', 36)))
        pg.display.set_caption("This is a roguelike project.")

    def updateScreen(self, sys):
        pass

    def determineAction(self, sys, event):
        pass
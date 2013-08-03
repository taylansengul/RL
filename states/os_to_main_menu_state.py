import pygame as pg
import data
from systems.cFontManager import cFontManager
from systems.graphics_engine import Graphics_Engine
from systems.io_handler import Io_Handler


class Enter_Main_Game_Loop_State(object):
    """Initialize graphics handler, main screen, game fonts and i/o handler"""
    def __init__(self, game):
        self.game = game
        self.name = 'initializing state'

    def init(self):
        print 'initializing graphics'  # initialize graphics engine handler
        self.game.graphics_engine = Graphics_Engine(self.game)
        print 'initializing io handler'  # initialize io handler
        self.game.io_handler = Io_Handler(self.game)
        # setup pygame
        pg.init()
        # initialize main screen
        self.game.graphics_engine.screens['main'] = pg.display.set_mode(data.Screens.screen_size['main'], 0, 32)
        # Setup fonts and font manager
        # avail_fonts = pg.font.get_fonts()
        # avail_fonts = ['arial']
        self.game.graphics_engine.font_18 = pg.font.SysFont(None, 18)
        self.game.graphics_engine.font_36 = pg.font.SysFont(None, 36)
        self.game.graphics_engine.fontMgr = cFontManager((('arial', 12), ('arial', 18), ('arial', 36)))
        pg.display.set_caption("This is a roguelike project.")

    def updateScreen(self):
        pass

    def determineAction(self):
        pass
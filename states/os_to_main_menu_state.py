import data
from systems.cFontManager import cFontManager
from systems.graphics_engine import Graphics_Engine
from systems.io_handler import Io_Handler
import random
import pygame


class Enter_Main_Game_Loop_State(object):
    """Initialize graphics handler, main screen, game fonts and i/o handler"""
    def __init__(self, game):
        self.game = game
        self.ID = 'initializing state'

    def init(self):
        print 'initializing graphics engine'
        self.game.graphics_engine = Graphics_Engine(self.game)
        print 'initializing i/o handler'
        self.game.io_handler = Io_Handler(self.game)
        print 'initializing random seed'
        seed_value = 0  # make this None to use the system time as a seed_value
        random.seed(seed_value)
        # setup pygame
        self.game.pygame = pygame
        self.game.pygame.init()
        # load data
        self.game.data = data
        # initialize main screen
        self.game.main_screen = self.game.pygame.display.set_mode(self.game.data.screens.screen_size['main'], 0, 32)
        # initialize main menu screen
        self.game.state_manager.initialize_screens('main_menu_state')
        # Setup fonts and font manager
        # avail_fonts = self.game.pygame.font.get_fonts()
        # avail_fonts = ['arial']
        self.game.graphics_engine.font_18 = self.game.pygame.font.SysFont(None, 18)
        self.game.graphics_engine.font_36 = self.game.pygame.font.SysFont(None, 36)
        self.game.font_manager = cFontManager((('arial', 12), ('arial', 18), ('arial', 36)))
        self.game.pygame.display.set_caption("This is a roguelike project.")

    def updateScreen(self):
        pass

    def determineAction(self):
        pass
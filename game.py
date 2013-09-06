from systems.state_manager import State_Manager
import data
from systems.graphics_engine import Graphics_Engine
from systems.io_handler import Io_Handler
import random
import pygame


class Game(object):
    def __init__(self):
        self.is_in_loop = True
        # initializing systems
        print 'Initializing Systems...',
        self.state_manager = State_Manager(self)
        # setup pygame
        self.pygame = pygame
        self.pygame.init()
        self.io_handler = Io_Handler(self)
        self.graphics_engine = Graphics_Engine(self)
        # Setup fonts
        self.graphics_engine.font_18 = self.pygame.font.SysFont(None, 18)
        self.graphics_engine.font_36 = self.pygame.font.SysFont(None, 36)
        # Load data
        self.data = data
        print 'done.'
        print 'initializing random seed'
        seed_value = 0  # make this None to use the system time as a seed_value
        random.seed(seed_value)
        # Main Screen
        self.main_screen = self.pygame.display.set_mode(self.data.screens.screen_size['main'], 0, 32)
        # initialize main menu screen
        self.state_manager.initialize_screens('main_menu_state')

        # initialized at main menu state:
        self.event_log = [None]
        self.time = None
        self.logger = None
        self.game_world = None
        self.ai = None
        self.objects_handler = None
        self.resource_manager = None
        # also player is created

    def loop(self):
        SM = self.state_manager
        while self.is_in_loop:
            # get input
            self.io_handler.compute_active_event()
            # if there is input
            if self.io_handler.active_event:
                # determine action
                SM.current_state.determineAction()
                # update graphics
                SM.current_state.updateScreen()

    def exit(self):
        # delete game engines
        print 'Exiting to OS.'

def main():
    game = Game()
    game.state_manager.change_state(game.state_manager.main_menu_state)
    game.loop()
    game.exit()
    del game


if __name__ == '__main__':
    main()
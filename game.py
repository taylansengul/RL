import random
import pygame
import globals as g
from systems.state_manager import State_Manager
from systems.io_handler import Io_Handler


class Game(object):
    def __init__(self):
        self.is_in_loop = True
        # initializing systems
        print 'Initializing Systems...',
        self.state_manager = State_Manager(self)
        pygame.init()
        self.io_handler = Io_Handler(self)
        # Setup fonts
        # done in graphics.fonts
        print 'done.'
        print 'initializing random seed'
        seed_value = 0  # make this None to use the system time as a seed_value
        random.seed(seed_value)
        # initialize main menu screen
        self.state_manager.initialize_screens(g.StateID.MAIN_MENU)

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
                # refresh
                self.refresh_main_screen()

    def refresh_main_screen(self):
        pygame.display.flip()

    def exit(self):
        # delete game engines
        print 'Exiting to OS.'
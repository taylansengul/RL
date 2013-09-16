import random
import pygame
from systems.io_handler import Io_Handler
import settings
import states
import graphics


class Game(object):
    def __init__(self):
        self.is_in_loop = True
        # initializing systems
        print 'Initializing Systems...',
        pygame.init()
        self.io_handler = Io_Handler(self)
        # Setup fonts
        # done in graphics.fonts
        print 'done.'
        print 'initializing random seed'
        seed_value = 0  # make this None to use the system time as a seed_value
        random.seed(seed_value)
        # initialize states
        self.main_menu_state = states.Main_Menu_State(self)
        self.map_state = states.Map_State(self)
        self.inventory_state = states.Inventory_State(self)
        self.game_over_screen_state = states.Game_Over_Screen_State(self)
        self.targeting_state = states.Targeting_State(self)
        self.current_state = None
        self._states = [self.main_menu_state, self.map_state, self.inventory_state, self.game_over_screen_state,
                        self.targeting_state]

        # initialize screens
        self._initialize_screens()
        # initialized at main menu state:
        self.event_log = [None]
        self.time = None
        self.game_world = None
        self.ai = None
        self.objects_handler = None
        self.resource_manager = None
        # also player is created

    def loop(self):
        while self.is_in_loop:
            # get input
            self.io_handler.compute_active_event()
            # if there is input
            if self.io_handler.active_event:
                # determine action
                self.current_state.determineAction()
                # update graphics
                self.current_state.updateScreen()
                # refresh
                self.refresh_main_screen()

    def change_state(self, new_state):
        self.current_state = new_state
        self.current_state.init()

    def _initialize_screens(self):
        D = settings.screen_settings.screens
        for a_screen_ID in D:
            if a_screen_ID == 'MAIN_SCREEN':
                continue
            a_state_ID = D[a_screen_ID]['state']
            state = self._get_state_by_ID(a_state_ID)
            state.screens[a_screen_ID] = graphics.screen.Screen(**D[a_screen_ID])

    def _get_state_by_ID(self, ID):
        for state in self._states:
            if state.ID == ID:
                return state

    def refresh_main_screen(self):
        pygame.display.flip()

    def exit(self):
        # delete game engines
        print 'Exiting to OS.'
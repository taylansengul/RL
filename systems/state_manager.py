from graphics import screen
import states
from settings import screen_settings


class State_Manager(object):
    def __init__(self, game):
        self.game = game
        self.main_menu_state = states.Main_Menu_State(game)
        self.map_state = states.Map_State(game)
        self.inventory_state = states.Inventory_State(game)
        self.game_over_screen_state = states.Game_Over_Screen_State(game)
        self.targeting_state = states.Targeting_State(game)
        self.current_state = None
        self._states = [self.main_menu_state, self.map_state, self.inventory_state, self.game_over_screen_state,
                        self.targeting_state]

    def change_state(self, new_state):
        self.current_state = new_state
        self.current_state.init()

    def initialize_screens(self, a_state_ID):
        D = screen_settings.screens
        state = self._get_state_by_ID(a_state_ID)
        for screen_ID in D:
            if D[screen_ID]['state'] == a_state_ID:
                state.screens[screen_ID] = screen.Screen(**D[screen_ID])


    def _get_state_by_ID(self, ID):
        for state in self._states:
            if state.ID == ID:
                return state
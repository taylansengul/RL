from graphics import screen
import states


class State_Manager(object):
    def __init__(self, game):
        self.game = game
        self.main_menu_state = states.Main_Menu_State(game)
        self.map_state = states.Map_State(game)
        self.inventory_state = states.Inventory_State(game)
        self.game_over_screen_state = states.Game_Over_Screen_State(game)
        self.targeting_state = states.Targeting_State(game)
        self.current_state = None
        self.states = [self.main_menu_state, self.map_state, self.inventory_state, self.game_over_screen_state,
                       self.targeting_state]

    def change_state(self, new_state):
        self.current_state = new_state
        self.current_state.init()

    def initialize_screens(self, state_ID):
        for state in self.states:
            if state.ID == state_ID:
                for screen_ID in self.game.data.screens.screen_size[state_ID]:
                    state.screens[screen_ID] = screen.Screen(self.game, **{'state': state_ID, 'name': screen_ID})
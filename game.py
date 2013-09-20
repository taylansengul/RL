from systems.IO import IO
import states


class Game(object):
    def __init__(self):
        self.is_in_loop = True
        # initialize states
        self.main_menu_state = states.Main_Menu_State(self)
        self.map_state = states.Map_State(self)
        self.inventory_state = states.Inventory_State(self)
        self.game_over_screen_state = states.Game_Over_Screen_State(self)
        self.targeting_state = states.Targeting_State(self)
        self.current_state = None
        self._states = [self.main_menu_state, self.map_state, self.inventory_state, self.game_over_screen_state,
                        self.targeting_state]

    def loop(self):
        while self.is_in_loop:
            # get input
            IO.compute_active_event(self.current_state.ID)
            # determine action
            self.current_state.determineAction()
            # update graphics
            self.current_state.updateScreen()

    def change_state(self, new_state):

        self.current_state = new_state
        self.current_state.init()

    def _get_state_by_ID(self, ID):
        for state in self._states:
            if state.ID == ID:
                return state

    def exit(self):
        # delete game engines
        print 'Exiting to OS.'
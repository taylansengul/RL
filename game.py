import states
import globals


class Game(object):

    def __init__(self):
        self.is_in_loop = True
        self.current_state = None
        self.states = {
            globals.MAIN_MENU_STATE: states.Main_Menu_State(),
            globals.MAP_STATE: states.Map_State(self),
            globals.INVENTORY_STATE: states.Inventory_State(),
            globals.GAME_OVER_STATE: states.Game_Over_Screen_State(),
            globals.TARGETING_STATE: states.Targeting_State(self)}

    def loop(self):
        prev_state_ID = None
        while self.is_in_loop:
            if not self.current_state.ID == prev_state_ID:
                self.current_state.init()
            prev_state_ID = self.current_state.ID
            self.current_state.run()
            next_state_ID = self.current_state.next_game_state
            if self.current_state.next_game_state == "QUIT_STATE":
                self.is_in_loop = False
            else:
                self.current_state = self.states[next_state_ID]

    def exit(self):
        print("Exit to OS")
        return

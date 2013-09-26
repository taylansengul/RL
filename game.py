import enums
import states


class Game(object):

    def __init__(self):
        self.current_state = None
        self.states = {
            enums.MAIN_MENU_STATE: states.MainMenuState(),
            enums.MAP_STATE: states.MapState(),
            enums.INVENTORY_STATE: states.InventoryState(),
            enums.GAME_OVER_STATE: states.GameOverScreenState(),
            enums.TARGETING_STATE: states.TargetingState()}

    def loop(self):
        parameters = {}
        state_changed = True
        while True:
            next_state, parameters = self.current_state.run(state_changed, parameters)
            if next_state == "QUIT_STATE":
                break
            if self.current_state.ID == next_state:
                state_changed = False
            else:
                state_changed = True
                self.current_state = self.states[next_state]

    @staticmethod
    def exit():
        print("Exit to OS")

import enums
from systems import draw
import base_state


class GameOverScreenState(base_state.BaseState):
    def __init__(self):
        super(GameOverScreenState, self).__init__(enums.GAME_OVER_STATE)

    def init(self):
        super(GameOverScreenState, self).init()
        self.update_screen()

    def determine_action(self):
        super(GameOverScreenState, self).determine_action()
        event = self.get_event()
        if event == 'pass':
            self.next_game_state = enums.MAIN_MENU_STATE

    def update_screen(self):
        draw.draw_game_over_messages()
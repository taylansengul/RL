from globals import *
from systems import draw
import base_state


class Game_Over_Screen_State(base_state.BaseState):
    def __init__(self):
        super(Game_Over_Screen_State, self).__init__(GAME_OVER_STATE)

    def init(self):
        self.update_screen()

    def determine_action(self):
        super(Game_Over_Screen_State, self).determine_action()
        event = self.get_event()
        if event == 'pass':
            self.next_game_state = MAIN_MENU_STATE

    def update_screen(self):
        draw.game_over_messages()
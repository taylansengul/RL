import states


class State_Manager(object):
    def __init__(self, game):
        self.game = game
        self.enter_game_loop_state = states.Enter_Main_Game_Loop_State(game)
        self.main_menu_state = states.Main_Menu_State(game)
        self.map_state = states.Map_State(game)
        self.exit_game_loop_state = states.Exit_Game_Loop_State(game)
        self.inventory_state = states.Inventory_State(game)
        self.main_menu_to_map_state = states.Main_Menu_To_Map_State(game)
        self.exit_to_os_state = states.Exit_To_OS_State(game)
        self.game_over_state = states.Game_Over_State(game)
        self.targeting_state = states.Targeting_State(game)
        self.current_state = None

    def change_state(self, new_state):
        self.current_state = new_state
        self.current_state.init()
from systems.state_manager import State_Manager


class Game(object):
    def __init__(self):
        self.state_manager = State_Manager(self)
        # initialized in os_to_main_menu_state
        self.io_handler = None
        self.graphics_engine = None
        self.font_manager = None
        self.is_in_loop = True

        # initialized in initializing_new_map_state
        self.main_screen = None
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


def main():
    game = Game()
    game.state_manager.change_state(game.state_manager.enter_game_loop_state)
    # since no input needed in initializing state, pass directly to main menu state
    game.state_manager.change_state(game.state_manager.main_menu_state)
    game.loop()
    game.state_manager.change_state(game.state_manager.exit_to_os_state)
    del game


if __name__ == '__main__':
    main()
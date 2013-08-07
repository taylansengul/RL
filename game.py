from systems.state_manager import State_Manager


class Game(object):
    def __init__(self):
        self.state_manager = State_Manager(self)
        # initialized in os_to_main_menu_state
        self.io_handler = None
        self.graphics_engine = None

        # initialized in initializing_new_map_state
        self.event_log = [None]
        self.time = None
        self.logger = None
        self.game_world = None
        self.ai = None
        self.objects_handler = None
        self.resource_manager = None
        # also player is created

    def loop(self):
        while not self.state_manager.current_state == self.state_manager.exit_game_loop_state:
            # get input
            self.io_handler.compute_active_event()
            # if there is input
            if self.io_handler.active_event:
                # determine action
                self.state_manager.current_state.determineAction()
                # update graphics
                self.graphics_engine.update_screen()


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
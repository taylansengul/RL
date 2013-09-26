__author__ = 'Taylan Sengul'
from systems.IO import IO


class BaseState(object):
    def __init__(self, ID):
        self.ID = ID
        self.next_game_state = ID
        self.parameters = None
        self.next_game_state_parameters = {}

    def get_event(self):
        IO.compute_active_event(self.ID)
        return IO.active_event

    def set_next_game_state(self, ID):
        self.next_game_state = ID

    def run(self, state_changed, parameters):
        self.parameters = parameters
        if state_changed:
            self.init()
        self.determine_action()
        self.update_screen()
        return self.next_game_state, self.next_game_state_parameters

    def init(self):
        """entering to this state"""
        pass

    def determine_action(self):
        self.next_game_state = self.ID
        pass

    def update_screen(self):
        pass

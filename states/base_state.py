__author__ = 'Taylan Sengul'
from systems.IO import IO


class BaseState(object):
    def __init__(self, ID):
        self.ID = ID
        self.next_game_state = ID

    def get_event(self):
        IO.compute_active_event(self.ID)
        return IO.active_event

    def set_next_game_state(self, ID):
        self.next_game_state = ID

    def run(self):
        self.determine_action()
        self.update_screen()

    def init(self):
        """entering to this state"""
        pass

    def determine_action(self):
        self.next_game_state = self.ID
        pass

    def update_screen(self):
        pass

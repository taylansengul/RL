__author__ = 'Taylan Sengul'
from systems.IO import IO


class BaseState(object):
    def __init__(self, ID):
        self.ID = ID
        self.next_game_state = ID
        self.incoming_keys = []
        self.incoming = {}
        self.outgoing = {}

    def get_event(self):
        IO.compute_active_event(self.ID)
        return IO.active_event

    def set_next_game_state(self, ID):
        self.next_game_state = ID

    def unpack_incoming(self, incoming):
        for key, val in incoming.iteritems():
            assert key in self.incoming_keys, "No key as %s" % key
            setattr(self, key, val)

    def run(self, state_changed, incoming):
        self.unpack_incoming(incoming)
        if state_changed:
            self.init()
        self.determine_action()
        self.update_screen()
        return self.next_game_state, self.outgoing

    def init(self):
        self.outgoing = {}
        """entering to this state from a different state"""
        pass

    def determine_action(self):
        self.next_game_state = self.ID
        pass

    def update_screen(self):
        pass

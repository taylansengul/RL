from systems.graphics.text import Text


class Time(object):
    def __init__(self, game):
        self.game = game
        self.turn = 1

    def new_turn(self):
        # update player status
        self.game.objects_handler.player.update_status()
        # player vision changes
        self.game.objects_handler.player.update_vision()
        # ai action
        # do not need ai: self.game.ai.determine_total_action()
        self.turn += 1
        # run resource manager
        self.game.resource_manager.manage()

    def render_turn(self):
        Text(screen=self.game.state_manager.map_state.screens['game info'],
             context='turn: %d' % self.turn, font= 'console', coordinates=(0, 0), color='white').render()
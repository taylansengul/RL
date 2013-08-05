import data


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

    def get_display_info(self):
        st = [{'screen': 'game info',
               'info': [{'item': 'turn: %d' % self.turn,
                         'coordinates': (0, 0),
                         'color': data.colors.palette['white']}]}]
        return st
import data


class Time(object):
    def __init__(self):
        self.turn = 1

    def new_turn(self):
        self.turn += 1

    def get_display_info(self):
        st = [{'screen': 'game info',
               'info': [{'item': 'turn: %d' % self.turn,
                         'coordinates': (0, 0),
                         'color': data.Colors.palette['white']}]}]
        return st
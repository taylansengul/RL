class Exit_To_OS_State(object):
    def __init__(self, game):
        self.game = game
        self.ID = 'exit to OS state'

    def init(self):
        # delete game engines
        print 'Exiting to OS.'

    def updateScreen(self):
        pass
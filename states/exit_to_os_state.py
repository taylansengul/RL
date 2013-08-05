class Exit_To_OS_State(object):
    def __init__(self, game):
        self.game = game
        self.id = 'exit to OS state'

    def init(self):
        # delete game engines
        del self.game.io_handler
        del self.game.graphics_engine
        print 'Exiting to OS.'

    def updateScreen(self):
        pass
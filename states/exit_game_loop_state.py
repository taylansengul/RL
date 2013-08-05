class Exit_Game_Loop_State(object):
    """Exit from Game Loop"""
    def __init__(self, game):
        self.game = game
        self.id = 'exit game loop state'

    def init(self):
        print 'Exiting Game Loop'

    def updateScreen(self):
        pass
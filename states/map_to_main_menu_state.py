class Map_To_Main_Menu_State(object):
    def __init__(self, game):
        self.game = game
        self.id = 'map to main state'

    def init(self):
        # delete game info
        del self.game.time
        del self.game.event_log
        del self.game.logger
        del self.game.game_world
        del self.game.ai

    def updateScreen(self):
        print 'Goodbye'
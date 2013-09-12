import globals as g
from graphics.text import Text


class Game_Over_Screen_State(object):
    def __init__(self, game):
        self.game = game
        self.ID = g.StateID.GAME_OVER
        self.screens = {g.ScreenID.GAME_OVER: None}

    def init(self):
        self.updateScreen()

    def determineAction(self):
        event = self.game.io_handler.get_active_event()
        if event == 'pass':
            self.game.change_state(self.game.main_menu_state)

    def updateScreen(self):
        screen = self.screens[g.ScreenID.GAME_OVER]
        screen.clear()
        self._render_game_over_messages()

    # PRIVATE METHODS
    def _render_game_over_messages(self):
        screen = self.screens[g.ScreenID.GAME_OVER]
        line_height = 40
        contexts = ['Game is over.',
                    self.game.logger.game_over_message,
                    'Press Space.']
        l = len(contexts)

        screens = [screen]*l
        coordinates = [(0, j*line_height) for j in range(l)]
        colors = ['white']*l
        for _ in zip(screens, contexts, coordinates, colors):
            t = Text(font=g.FontID.CONSOLE, screen=_[0], context=_[1], coordinates=_[2], color=_[3])
            t.render()
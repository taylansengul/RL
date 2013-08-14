import data


class Game_Over_State(object):
    def __init__(self, game):
        self.game = game
        self.ID = 'game over state'

    def init(self):
        pass

    def determineAction(self):
        event = self.game.io_handler.get_active_event()
        if event == 'pass':
            self.game.state_manager.change_state(self.game.state_manager.main_menu_state)

    def updateScreen(self):
        graphics = self.game.graphics_engine
        graphics.screens['main'].fill(data.colors.palette['black'])
        graphics.font_manager.Draw(graphics.screens['main'], 'arial', 36, 'Game is over.',
            (0, 0), data.colors.palette['white'], 'center', 'center', True)
        graphics.font_manager.Draw(graphics.screens['main'], 'arial', 36, self.game.logger.game_over_message,
            (0, 40), data.colors.palette['white'], 'center', 'center', True)
        graphics.font_manager.Draw(graphics.screens['main'], 'arial', 36, 'Press Space.',
            (0, 80), data.colors.palette['white'], 'center', 'center', True)
        self.game.pygame.display.flip()
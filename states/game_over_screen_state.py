import data


class Game_Over_Screen_State(object):
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
        info = [{'screen': 'main',
                 'info': [{'item': 'Game is over.', 'coordinates': (0, 0), 'color': data.colors.palette['white']},
                          {'item': self.game.logger.game_over_message, 'coordinates': (0, 40), 'color': data.colors.palette['white']},
                          {'item': 'Press Space.', 'coordinates': (0, 80), 'color': data.colors.palette['white']}]}]
        self.game.graphics_engine.render_info(info)
        self.game.pygame.display.flip()
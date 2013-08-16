import data
from systems.graphics.text import Text


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
        info = []
        line_height = 40
        contexts = ['Game is over.',
                    self.game.logger.game_over_message,
                    'Press Space.']
        l = len(contexts)
        screen_IDs = ['main']*l
        coordinates = [(0, j*line_height) for j in range(l)]
        colors = ['white']*l
        for _ in zip(screen_IDs, contexts, coordinates, colors):
            info.append(Text(screen=_[0], context=_[1], coordinates=_[2], color=_[3]))

        self.game.graphics_engine.screens['main'].fill(data.colors.palette['black'])
        self.game.graphics_engine.render_info(info)
        self.game.pygame.display.flip()
import data
from systems.graphics.text import Text


class Game_Over_Screen_State(object):
    def __init__(self, game):
        self.game = game
        self.ID = 'game_over_screen_state'
        self.screens = {'main': None}

    def init(self):

        self.game.main_screen.fill((0, 0, 0))
        self.game.state_manager.initialize_screens(self.ID)
        self.updateScreen()

    def determineAction(self):
        event = self.game.io_handler.get_active_event()
        if event == 'pass':
            self.game.state_manager.change_state(self.game.state_manager.main_menu_state)

    def updateScreen(self):
        screen = self.screens['main']
        screen.clear()
        self.render_game_over_messages()
        screen.render()
        self.game.pygame.display.update()

    def render_game_over_messages(self):
        screen = self.screens['main']
        line_height = 40
        contexts = ['Game is over.',
                    self.game.logger.game_over_message,
                    'Press Space.']
        l = len(contexts)

        screens = [screen]*l
        coordinates = [(0, j*line_height) for j in range(l)]
        colors = ['white']*l
        for _ in zip(screens, contexts, coordinates, colors):
            Text(self.game, screen=_[0], context=_[1], coordinates=_[2], color=_[3]).render()
        self.game.pygame.draw.rect(screen.surface, (255, 255, 255), (10, 10, 100, 100))
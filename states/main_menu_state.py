from systems.graphics.menu import Menu, Menu_Option
import data


class Main_Menu_State(object):
    def __init__(self, game):
        self.game = game
        self.ID = 'main menu state'
        self.screens = {'menu': None}

    def init(self):
        font = self.game.graphics_engine.font_18
        self.newGameOption = Menu_Option("NEW GAME", (140, 105), font, isHovered=True)
        self.loadGameOption = Menu_Option("LOAD GAME", (140, 155), font)
        self.quitGameOption = Menu_Option("QUIT", (140, 205), font)
        self.menu = Menu(screen=self.screens['menu'],
                         options=[self.newGameOption,
                                  self.loadGameOption,
                                  self.quitGameOption])
        self.updateScreen()

    def updateScreen(self):
        self.menu.draw()
        self.screens['menu'].render()
        self.game.pygame.display.update()

    def determineAction(self):
        event = self.game.io_handler.get_active_event()
        if event == 'down':
            self.menu.select_next()
        elif event == 'up':
            self.menu.select_prev()
        elif event == 'select':
            option = self.menu.get_active_option()
            if option == self.newGameOption:
                self.game.state_manager.change_state(self.game.state_manager.main_menu_to_map_state)
                self.game.state_manager.change_state(self.game.state_manager.map_state)
            elif option == self.loadGameOption:
                pass
            elif option == self.quitGameOption:
                self.game.is_in_loop = False
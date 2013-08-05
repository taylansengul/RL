import pygame as pg
from systems.graphics.menu import Menu, Menu_Option
import data


class Main_Menu_State(object):
    def __init__(self, game):
        self.game = game
        self.name = 'main menu state'

    def init(self):
        gE = self.game.graphics_engine
        gE.screens['main'].fill(data.colors.palette['black'])
        gE.screens['menu'] = pg.Surface(data.screens.screen_size['main menu state'])
        font = gE.font_18
        self.newGameOption = Menu_Option("NEW GAME", (140, 105), font, isHovered=True)
        self.loadGameOption = Menu_Option("LOAD GAME", (140, 155), font)
        self.quitGameOption = Menu_Option("QUIT", (140, 205), font)
        self.menu = Menu(screen=gE.screens['menu'],
                         options=[self.newGameOption,
                                  self.loadGameOption,
                                  self.quitGameOption])
        self.updateScreen()

    def updateScreen(self):
        gE = self.game.graphics_engine
        self.menu.draw()
        gE.screens['main'].blit(gE.screens['menu'], data.screens.screen_coordinates['main menu state'])
        pg.display.update()

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
                self.game.state_manager.change_state(self.game.state_manager.exit_game_loop_state)
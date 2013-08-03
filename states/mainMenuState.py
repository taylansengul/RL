import pygame as pg
from systems.graphics.menu import Menu, Menu_Option
import data


class MainMenuState(object):
    def __init__(self):
        self.name = 'main menu state'

    def init(self, sys):
        sys.graphics_engine.screens['menu'] = pg.Surface(data.Screens.screen_size['main menu state'])
        font = sys.graphics_engine.font_18
        self.newGameOption = Menu_Option("NEW GAME", (140, 105), font, isHovered=True)
        self.loadGameOption = Menu_Option("LOAD GAME", (140, 155), font)
        self.quitGameOption = Menu_Option("QUIT", (140, 205), font)
        self.menu = Menu(screen=sys.graphics_engine.screens['menu'],
                         options=[self.newGameOption,
                                  self.loadGameOption,
                                  self.quitGameOption])
        self.updateScreen(sys)

    def updateScreen(self, sys):
        gE = sys.graphics_engine
        self.menu.draw()
        gE.screens['main'].blit(gE.screens['menu'], data.Screens.screen_coordinates['main menu state'])
        pg.display.update()

    def determineAction(self, sys, event):
        if event == 'down':
            self.menu.select_next()
        elif event == 'up':
            self.menu.select_prev()
        elif event == 'select':
            option = self.menu.get_active_option()
            if option == self.newGameOption:
                sys.stateManager.changeState(sys.stateManager.mapState, sys)
            elif option == self.loadGameOption:
                pass
            elif option == self.quitGameOption:
                sys.stateManager.changeState(sys.stateManager.quittingState, sys)
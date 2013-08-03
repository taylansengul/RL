import pygame as pg
import data
from systems.cFontManager import cFontManager


class InventoryState(object):
    def __init__(self, inventory=[]):
        self.name = 'inventory state'
        self.inventory = inventory

    def init(self, sys):
        gE = sys.graphics_engine
        self. inventory = sys.game_world.objects.player.inventory
        # screens
        gE.screens['inventory state'] = pg.Surface(data.Screens.screen_size['inventory state'])
        # Setup the Font
        # avail_fonts = pg.font.get_fonts()
        # avail_fonts = ['arial']
        gE.font_18 = pg.font.SysFont(None, 18)
        gE.font_36 = pg.font.SysFont(None, 36)
        gE.fontMgr = cFontManager((('arial', 12), ('arial', 18), ('arial', 36)))
        pg.display.set_caption("This is a roguelike project.")

    def updateScreen(self, sys):
        gE = sys.graphics_engine
        screen = gE.screens['inventory state']
        screen.fill(data.Colors.palette['black'])
        if self.inventory:
            for item in self.inventory:
                gE.fontMgr.Draw(screen, 'arial', 36, item.name, (0, 0), data.Colors.palette['white'], 'center', 'center', True)
        gE.screens['main'].blit(screen, (0, 0))
        pg.display.flip()

    def determineAction(self, sys, event):
        if event == 'quit':
            sys.stateManager.changeState(sys.stateManager.mapState, sys)
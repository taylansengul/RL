import pygame as pg
import data
from systems.cFontManager import cFontManager


class Inventory_State(object):
    def __init__(self, game):
        self.name = 'inventory state'
        self.game = game
        self.inventory = None  # to be initialized later

    def init(self):
        self.inventory = self.game.objects_handler.player.objects

    def updateScreen(self):
        gE = self.game.graphics_engine
        screen = gE.screens['inventory state']
        screen.fill(data.Colors.palette['black'])
        if self.inventory:
            for item in self.inventory:
                if 'stackable' in item.properties:
                    gE.fontMgr.Draw(screen, 'arial', 36, item.name + str(item.quantity),
                                    (0, 0), data.Colors.palette['white'], 'center', 'center', True)
                else:
                    gE.fontMgr.Draw(screen, 'arial', 36, item.name,
                                    (0, 0), data.Colors.palette['white'], 'center', 'center', True)
        else:
            gE.fontMgr.Draw(screen, 'arial', 36, 'Empty Inventory',
                            (0, 0), data.Colors.palette['white'], 'center', 'center', True)

        gE.screens['main'].blit(screen, (0, 0))
        pg.display.flip()

    def determineAction(self):
        event = self.game.io_handler.get_active_event()
        if event == 'quit':
            self.game.state_manager.change_state(self.game.state_manager.map_state)
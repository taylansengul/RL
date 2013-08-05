import pygame as pg
import data


class Inventory_State(object):
    def __init__(self, game):
        self.id = 'inventory state'
        self.game = game
        self.inventory = None  # to be initialized later

    def init(self):
        self.inventory = self.game.objects_handler.player.objects

    def updateScreen(self):
        gE = self.game.graphics_engine
        screen = gE.screens['inventory state']
        screen.fill(data.colors.palette['black'])
        st = 30
        if self.inventory:
            for j, item in enumerate(self.inventory):
                if 'stackable' in item.properties:
                    gE.fontMgr.Draw(screen, 'arial', 36, item.id + ' ' + str(item.quantity),
                                    (0, j*st), data.colors.palette['white'], 'center', 'center', True)
                else:
                    gE.fontMgr.Draw(screen, 'arial', 36, item.id,
                                    (0, j*st), data.colors.palette['white'], 'center', 'center', True)
        else:
            gE.fontMgr.Draw(screen, 'arial', 36, 'Empty Inventory',
                            (0, 0), data.colors.palette['white'], 'center', 'center', True)

        gE.screens['main'].blit(screen, (0, 0))
        pg.display.flip()

    def determineAction(self):
        event = self.game.io_handler.get_active_event()
        if event == 'quit':
            self.game.state_manager.change_state(self.game.state_manager.map_state)
        if event == 'eat item':
            self.inventory = self.game.objects_handler.player.get_objects('edible')
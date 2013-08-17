import data
from systems.graphics.menu import Menu, Menu_Option


# todo: create inventory state main screen
class Inventory_State(object):
    def __init__(self, game):
        self.ID = 'inventory state'
        self.game = game
        self.inventory = None  # to be initialized later
        self.selected_item = None
        self.menu_options = []
        self.key = ''
        self.screens = {'menu': None, 'details': None}

    def init(self):
        self.inventory = self.game.objects_handler.player.get_objects(self.key)
        self.selected_item = None
        self.menu_options = []
        font = self.game.graphics_engine.font_18
        st = 18
        for j, item in enumerate(self.inventory):
            if 'stackable' in item.properties:
                label = str(item.quantity) + ' ' + item.ID
            else:
                label = item.ID
            if j == 0:
                self.menu_options.append(Menu_Option(label, (0, j * st), font, isHovered=True))
            else:
                self.menu_options.append(Menu_Option(label, (0, j * st), font))

        self.menu = Menu(screen=self.screens['menu'], options=self.menu_options)
        self.updateScreen()

    def updateScreen(self):
        screen = self.screens['menu']
        if self.inventory:
            self.menu.draw()
        else:
            self.game.main_screen.fill((0, 0, 0))
            self.game.font_manager.Draw(screen, 'arial', 36, 'Empty Inventory',
                            (0, 0), data.colors.palette['white'], 'center', 'center', True)

        screen.render()
        self.game.pygame.display.flip()

    def determineAction(self):
        self.selected_item = None
        event = self.game.io_handler.get_active_event()
        if self.inventory:
            if event == 'down':
                self.menu.select_next()
            elif event == 'up':
                self.menu.select_prev()
            elif event == 'select':
                option = self.menu.get_active_option()
                if option:  # if an option is hovered
                    item_index = self.menu_options.index(option)
                    self.selected_item = self.inventory[item_index]
            elif event == 'show edible items':
                self.key = 'edible'
                self.init()
            elif event == 'show consumable items':
                self.key = 'consumable'
                self.init()
            elif event == 'quit':
                self.game.state_manager.change_state(self.game.state_manager.map_state)
        else:
            if event == 'quit':
                self.game.state_manager.change_state(self.game.state_manager.map_state)

        if self.key == 'edible' and self.selected_item:
            self.game.objects_handler.player.consume(self.selected_item)
            self.game.state_manager.change_state(self.game.state_manager.map_state)
        elif self.key == 'consumable' and self.selected_item:
            self.game.objects_handler.player.consume(self.selected_item)
            self.game.state_manager.change_state(self.game.state_manager.map_state)
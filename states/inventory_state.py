from systems.graphics.menu import Menu, Menu_Option
from systems.graphics.text import Text


# todo: create inventory state main screen
class Inventory_State(object):
    def __init__(self, game):
        self.ID = 'inventory state'
        self.game = game
        self.inventory = None  # to be initialized later
        self.highlighted_item = None
        self.selected_item = None
        self.menu_options = []
        self.key = ''
        self.screens = {'menu': None, 'details': None}

    def init(self):
        self.inventory = self.game.objects_handler.player.get_objects(self.key)
        if self.inventory:
            self.highlighted_item = self.inventory[0]
        else:
            self.highlighted_item = None
        self.selected_item = None
        self.menu_options = []
        self._build_menu_from_inventory()  # builds menu from self.inventory
        self.updateScreen()

    def determineAction(self):
        self.selected_item = None
        event = self.game.io_handler.get_active_event()
        if self.inventory:  # if inventory is non-empty
            if event == 'down':
                self.menu.select_next()
                option = self.menu.get_active_option()
                if option:  # if an option is hovered
                    item_index = self.menu_options.index(option)
                    self.highlighted_item = self.inventory[item_index]
            elif event == 'up':
                self.menu.select_prev()
                option = self.menu.get_active_option()
                if option:  # if an option is hovered
                    item_index = self.menu_options.index(option)
                    self.highlighted_item = self.inventory[item_index]
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
        else:  # if inventory is empty
            if event == 'quit':
                self.game.state_manager.change_state(self.game.state_manager.map_state)

        if self.key == 'edible' and self.selected_item:
            self.game.objects_handler.player.consume(self.selected_item)
            self.game.state_manager.change_state(self.game.state_manager.map_state)
        elif self.key == 'consumable' and self.selected_item:
            self.game.objects_handler.player.consume(self.selected_item)
            self.game.state_manager.change_state(self.game.state_manager.map_state)

    def updateScreen(self):
        screen = self.screens['menu']
        screen.clear()
        self._render_inventory()
        screen.render()
        if self.inventory:
            screen = self.screens['details']
            screen.clear()
            self._render_item_properties()
            screen.render()
        self.game.pygame.display.flip()

    # PRIVATE METHODS
    def _build_menu_from_inventory(self):
        """Builds a menu object from self.inventory"""
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

    def _render_inventory(self):
        """Renders inventory if inventory not empty otherwise display a message to self.screens['menu']"""
        screen = self.screens['menu']
        if self.inventory:
            self.menu.draw()
        else:
            Text(self.game, screen=screen, context='Empty Inventory', coordinates=(0, 0), color='white').render()

    def _render_item_properties(self):
        screen = self.screens['details']
        context = self.highlighted_item.description
        Text(self.game, screen=screen, context=context, coordinates=(0, 0), color='white').render()
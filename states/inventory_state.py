from graphics.menu import Menu, Menu_Option
from graphics.text import Text
from inventory_state_screen_updater import InventoryStateScreenUpdater

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
        self.screen_updater = InventoryStateScreenUpdater(game, self.screens, )

    def init(self):
        self.inventory = self.game.objects_handler.player.get_objects(self.key)
        if self.inventory:
            self.highlighted_item = self.inventory[0]
        else:
            self.highlighted_item = None
        self.selected_item = None
        self.menu_options = []
        self._build_menu_from_inventory()
        self.updateScreen()

    def determineAction(self):
        self.selected_item = None
        event = self.game.io_handler.get_active_event()
        menu_actions = {
            None: self._none,
            'down': self._down,
            'up': self._up,
            'select': self._select,
            'show edible items': self._show_edible_items,
            'show consumable items': self._show_consumable_items,
            'quit': self._quit
        }
        if self.inventory:  # if inventory is non-empty
            menu_actions[event]()
        else:  # if inventory is empty
            if event == 'quit':
                self._quit()

        if self.selected_item:
            if self.key == 'edible':
                self.game.objects_handler.player.consume(self.selected_item)
                self.game.state_manager.change_state(self.game.state_manager.map_state)
            elif self.key == 'consumable':
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
    def _none(self):
        pass

    def _down(self):
        self.menu.select_next()
        option = self.menu.get_active_option()
        if option:  # if an option is hovered
            item_index = self.menu_options.index(option)
            self.highlighted_item = self.inventory[item_index]

    def _up(self):
        self.menu.select_prev()
        option = self.menu.get_active_option()
        if option:  # if an option is hovered
            item_index = self.menu_options.index(option)
            self.highlighted_item = self.inventory[item_index]

    def _select(self):
        option = self.menu.get_active_option()
        if option:  # if an option is hovered
            item_index = self.menu_options.index(option)
            self.selected_item = self.inventory[item_index]

    def _show_edible_items(self):
        self.key = 'edible'
        self.init()

    def _show_consumable_items(self):
        self.key = 'consumable'
        self.init()

    def _quit(self):
        self.game.state_manager.change_state(self.game.state_manager.map_state)


    def _build_menu_from_inventory(self):
        """Builds a menu object from self.inventory"""
        font = self.game.data.fonts.INVENTORY
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
        """Renders inventory if inventory is not empty otherwise display a message to self.screens['menu']"""
        screen = self.screens['menu']
        if self.inventory:
            self.menu.draw()
        else:  # inventory is empty
            t = Text(screen=screen, font='inventory', context='Empty Inventory', coordinates=(0, 0), color='white')
            t.render()

    def _render_item_properties(self):
        screen = self.screens['details']
        context = self.highlighted_item.description
        t = Text(font='inventory', screen=screen, context=context, coordinates=(0, 0), color='white')
        t.render()
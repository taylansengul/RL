from globals import *
from graphics.menu import Menu
from inventory_state_screen_updater import InventoryStateScreenUpdater


class Inventory_State(object):
    def __init__(self, game):
        self.ID = StateID.INVENTORY
        self.game = game
        self.inventory = None  # to be initialized later
        self.selected_item = None
        self.key = ''
        self.screens = {ScreenID.INVENTORY_MENU: None, ScreenID.INVENTORY_DETAILS: None}
        # todo: screen_updater
        self.screen_updater = InventoryStateScreenUpdater(game, self.screens)

    @property
    def highlighted_item(self):
        if len(self.inventory) == 0:
            return None
        else:
            return self.inventory[self.menu.highlighted_option_index]

    def init(self):
        self.inventory = self.game.objects_handler.player.get_objects(self.key)
        self.selected_item = None
        self._new_menu()
        self.updateScreen()

    def determineAction(self):
        self.selected_item = None
        event = self.game.io_handler.get_active_event()
        menu_actions = {
            None: self._none,
            'down': self._next,
            'up': self._prev,
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
        self.screen_updater.run()

    # PRIVATE METHODS
    def _none(self):
        pass

    def _next(self):
        self.menu.next()

    def _prev(self):
        self.menu.prev()

    def _select(self):
        self.selected_item = self.highlighted_item

    def _show_edible_items(self):
        self.key = 'edible'
        self.init()

    def _show_consumable_items(self):
        self.key = 'consumable'
        self.init()

    def _quit(self):
        self.game.state_manager.change_state(self.game.state_manager.map_state)

    def _new_menu(self):
        """Builds a menu object from self.inventory"""
        menu_options = [item.inventory_repr for item in self.inventory]
        self.menu = Menu(
            screen=self.screens[ScreenID.INVENTORY_MENU],
            options=menu_options,
            font=FontID.INVENTORY,
            empty_menu_message='Empty Inventory')
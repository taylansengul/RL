from globals import *
from graphics.menu import Menu
from entities.entity import Entity
from systems.IO import IO


class Inventory_State(object):
    """Inventory State of the game"""
    def __init__(self, game):
        self.ID = INVENTORY_STATE
        self.game = game
        self.inventory_objects_list = None
        self.selected_item = None
        self.key = ''
        self.menu = None
        self.screens = {INVENTORY_MENU_SCREEN: None, INVENTORY_DETAILS_SCREEN: None}

    @property
    def highlighted_item(self):
        if len(self.inventory_objects_list) == 0:
            return None
        else:
            index = self.menu.highlighted_option_index
            return self.inventory_objects_list[index]

    def init(self):
        self.inventory_objects_list = self._new_inventory_objects_list()
        self.selected_item = None
        self.menu = self._new_menu()
        self.updateScreen()
        # force a screen update
        screen = self.screens[INVENTORY_MENU_SCREEN]
        screen.force_screen_update()

    def determineAction(self):
        self.selected_item = None
        event = IO.get_active_event()
        menu_actions = {
            None: self._none,
            'down': self._next,
            'up': self._prev,
            'select': self._select,
            'show edible items': self._show_edible_items,
            'show consumable items': self._show_consumable_items,
            'quit': self._go_to_map_state
        }
        if self.inventory_objects_list:  # if inventory_objects_list is non-empty
            menu_actions[event]()
        else:  # if inventory_objects_list is empty
            if event == 'quit':
                self._go_to_map_state()

        if self.selected_item:
            if self.key == 'edible':
                Entity.player.consume(self.selected_item)
            elif self.key == 'consumable':
                Entity.player.consume(self.selected_item)

            self._go_to_map_state()

    def updateScreen(self):
        self._render_inventory_menu()
        self._render_highlighted_item_description()

    # PRIVATE METHODS
    # ---- ACTIONS ----
    def _go_to_map_state(self):
        self.game.change_state(self.game.map_state)

    def _next(self):
        self.menu.next()

    def _none(self):
        pass

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

    # ---------------------

    def _new_menu(self):
        """
        Builds a menu object from self.inventory_objects_list and returns it
        Return:
        -- Menu object
        """
        menu_options = [item.inventory_repr for item in self.inventory_objects_list]
        return Menu(
            screen=self.screens[INVENTORY_MENU_SCREEN],
            options=menu_options,
            font=INVENTORY_FONT,
            empty_menu_message='Empty Inventory')

    def _new_inventory_objects_list(self):
        return Entity.player.container.get(properties=self.key, key='all')

    # ----- SCREEN UPDATE ------
    def _render_inventory_menu(self):
        """render inventory_objects_list menu to """
        self.menu.render()

    def _render_highlighted_item_description(self):
        if not self.highlighted_item:
            return
        screen = self.screens[INVENTORY_DETAILS_SCREEN]
        self.highlighted_item.render_description_to(screen)
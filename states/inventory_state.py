from globals import *
from graphics.menu import Menu
from entities.entity import Entity
from systems.IO import IO

DEFAULT_STATE = 'DEFAULT_STATE'
CHOOSING_ITEM_FROM_MAP_STATE = 'CHOOSING_ITEM_FROM_MAP_STATE'
DEFAULT_WITH_EMPTY_INVENTORY_STATE = 'DEFAULT_WITH_EMPTY_INVENTORY_STATE'
SHOW_EDIBLE_ITEMS_STATE = 'SHOW_EDIBLE_ITEMS_STATE'
SHOW_CONSUMABLE_ITEMS_STATE = 'SHOW_CONSUMABLE_ITEMS_STATE'


class Inventory_State(object):
    """Inventory State of the game"""
    def __init__(self, game):
        self.current_state = DEFAULT_STATE
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
        choosing_actions = {
            None: self._none,
            'down': self._next,
            'up': self._prev,
            'select': self._select
        }
        menu_actions = {
            CHOOSING_ITEM_FROM_MAP_STATE: choosing_actions,
            DEFAULT_STATE: {
                None: self._none,
                'down': self._next,
                'up': self._prev,
                'show edible items': self._show_edible_items,
                'show consumable items': self._show_consumable_items,
                'quit': self._go_to_map_state
            },
            SHOW_EDIBLE_ITEMS_STATE: choosing_actions,
            SHOW_CONSUMABLE_ITEMS_STATE: choosing_actions,
            DEFAULT_WITH_EMPTY_INVENTORY_STATE: {
                'quit': self._go_to_map_state
            }
        }
        print self.current_state, event
        menu_actions[self.current_state][event]()

        if self.selected_item:
            if self.current_state == CHOOSING_ITEM_FROM_MAP_STATE:
                self._go_to_map_state()
            elif self.current_state == SHOW_EDIBLE_ITEMS_STATE:
                Entity.player.consume(self.selected_item)
                self._go_to_map_state()
            elif self.current_state == SHOW_CONSUMABLE_ITEMS_STATE:
                Entity.player.consume(self.selected_item)
                self._go_to_map_state()

    def updateScreen(self):
        self._render_inventory_menu()
        self._render_highlighted_item_description()

    # PRIVATE METHODS
    # ---- ACTIONS ----
    def _go_to_map_state(self):
        self.game.change_state(self.game.map_state)
        self.current_state = DEFAULT_STATE

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
        self.current_state = SHOW_EDIBLE_ITEMS_STATE
        self.init()

    def _show_consumable_items(self):
        self.key = 'consumable'
        self.current_state = SHOW_CONSUMABLE_ITEMS_STATE
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
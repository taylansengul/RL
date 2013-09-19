from globals import *
from graphics.menu import Menu
from entities.entity import Entity
from systems.IO import IO
from systems import draw

DEFAULT_STATE = 'DEFAULT_STATE'
CHOOSING_ITEM_FROM_MAP_STATE = 'CHOOSING_ITEM_FROM_MAP_STATE'
EMPTY_STATE = 'EMPTY_STATE'
SHOWING_EDIBLE_ITEMS_STATE = 'SHOWING_EDIBLE_ITEMS_STATE'
SHOWING_CONSUMABLE_ITEMS_STATE = 'SHOWING_CONSUMABLE_ITEMS_STATE'


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
        if len(self.inventory_objects_list) == 0:
            self.current_state = EMPTY_STATE
        self.selected_item = None
        self.change_state_flag = False
        self.menu = self._new_menu()
        self.updateScreen()
        # force a screen update
        screen = self.screens[INVENTORY_MENU_SCREEN]
        screen.force_screen_update()

    def process_event(self, user_input):
        choosing_actions = {
            'down': self._down,
            'up': self._up,
            'select': self._select,
            'quit': self.escape_state
        }
        menu_actions = {
            CHOOSING_ITEM_FROM_MAP_STATE: choosing_actions,
            DEFAULT_STATE: {
                'down': self._down,
                'up': self._up,
                'show edible items': self._show_edible_items,
                'show consumable items': self._show_consumable_items,
                'quit': self.escape_state
            },
            SHOWING_EDIBLE_ITEMS_STATE: choosing_actions,
            SHOWING_CONSUMABLE_ITEMS_STATE: choosing_actions,
            EMPTY_STATE: {
                'quit': self.escape_state
            }
        }
        if user_input in menu_actions[self.current_state]:
            print user_input, menu_actions[self.current_state].keys()
            menu_actions[self.current_state][user_input]()

    def change_state(self):
        if self.current_state == CHOOSING_ITEM_FROM_MAP_STATE:
            self.game.change_state(self.game.map_state)
            self.key = ''
            self.current_state = DEFAULT_STATE
        elif self.current_state == SHOWING_EDIBLE_ITEMS_STATE:
            if self.selected_item:
                Entity.player.consume(self.selected_item)
            self.key = ''
            self.current_state = DEFAULT_STATE
            self.init()
        elif self.current_state == SHOWING_CONSUMABLE_ITEMS_STATE:
            if self.selected_item:
                Entity.player.consume(self.selected_item)
            self.key = ''
            self.current_state = DEFAULT_STATE
            self.init()
        elif self.current_state == DEFAULT_STATE:
            self.game.change_state(self.game.map_state)
            self.key = ''
        elif self.current_state == EMPTY_STATE:
            self.game.change_state(self.game.map_state)
            self.key = ''
            self.current_state = DEFAULT_STATE

    def determineAction(self):
        user_input = IO.active_event  # get user_input
        self.process_event(user_input)
        if self.selected_item or self.change_state_flag:
            self.change_state()

    def updateScreen(self):
        self._render_inventory_menu()
        self._render_highlighted_item_description()
        draw.update()

    # PRIVATE METHODS
    # ---- ACTIONS ----
    def escape_state(self):
        self.change_state_flag = True

    def _down(self):
        self.menu.next()

    def _up(self):
        self.menu.prev()

    def _select(self):
        self.selected_item = self.highlighted_item

    def _show_edible_items(self):
        self.key = 'edible'
        self.current_state = SHOWING_EDIBLE_ITEMS_STATE
        self.init()

    def _show_consumable_items(self):
        self.key = 'consumable'
        self.current_state = SHOWING_CONSUMABLE_ITEMS_STATE
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
        draw.menu(self.menu)

    def _render_highlighted_item_description(self):
        if not self.highlighted_item:
            return
        screen = self.screens[INVENTORY_DETAILS_SCREEN]
        draw.description(self.highlighted_item, screen)
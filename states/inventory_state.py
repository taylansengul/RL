import enums
from graphics.menu import Menu
from entities.entity import Entity
from systems import draw
import base_state


DEFAULT_STATE = 'DEFAULT_STATE'
CHOOSING_ITEM_FROM_MAP_STATE = 'CHOOSING_ITEM_FROM_MAP_STATE'
EMPTY_STATE = 'EMPTY_STATE'
SHOWING_EDIBLE_ITEMS_STATE = 'SHOWING_EDIBLE_ITEMS_STATE'
SHOWING_CONSUMABLE_ITEMS_STATE = 'SHOWING_CONSUMABLE_ITEMS_STATE'


class InventoryState(base_state.BaseState):
    """Inventory State of the game"""

    def __init__(self):
        super(InventoryState, self).__init__(enums.INVENTORY_STATE)
        self.current_state = DEFAULT_STATE
        self.selected_item = None
        self.key = ''
        self.menu = None
        self.escape_pressed = False
        self.items_list = None

    @property
    def highlighted_item(self):
        if len(self.items_list) == 0:
            return None
        else:
            index = self.menu.highlighted_option_index
            return self.items_list[index]

    def init(self):
        """create a new inventory state using self.key"""
        self.key = self.parameters.get('inventory_key', None)
        self.current_state = self.parameters.get('state', DEFAULT_STATE)
        inventory = Entity.player.container
        self.items_list = inventory.get(properties=self.key, key='all')
        if len(self.items_list) == 0:
            self.current_state = EMPTY_STATE
        self.selected_item = None
        self.escape_pressed = False
        self.menu = self._new_menu()
        self.update_screen()

    def determine_action(self):
        super(InventoryState, self).determine_action()
        event = self.get_event()
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
        if event in menu_actions[self.current_state]:
            menu_actions[self.current_state][event]()

        if self.selected_item or self.escape_pressed:
            self._change_state()

    def update_screen(self):
        """render 1. items_list menu, 2.description of highlighted item,
        3. update screen"""
        draw.inventory_menu(self.menu)
        draw.inventory_description(self.highlighted_item)
        draw.update()

    # ============PRIVATE METHODS============
    def _reset(self):
        self.key = ''
        self.current_state = DEFAULT_STATE

    def _change_game_state(self):
        self.next_game_state = enums.MAP_STATE
        if self.selected_item:
            self.next_game_state_parameters = dict(selected_item=self.selected_item)
        self._reset()

    def _change_local_state(self):
        self._reset()
        self.init()

    def _change_state(self):
        # change game state
        states1 = [CHOOSING_ITEM_FROM_MAP_STATE, DEFAULT_STATE, EMPTY_STATE]
        if self.current_state in states1:
            self._change_game_state()
        # change local state
        elif self.current_state == SHOWING_EDIBLE_ITEMS_STATE:
            if self.selected_item:
                Entity.player.consume(self.selected_item)
            self._change_local_state()
        elif self.current_state == SHOWING_CONSUMABLE_ITEMS_STATE:
            if self.selected_item:
                Entity.player.consume(self.selected_item)
            self._change_local_state()

    # ---- ACTIONS ----
    def escape_state(self):
        self.escape_pressed = True

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

    def _new_menu(self):
        """
        Builds a menu object from self.items_list and returns it
        Return:
        -- Menu object
        """
        menu_options = [item.inventory_repr
                        for item in self.items_list]
        return Menu(
            screen=enums.INVENTORY_MENU_SCREEN,
            options=menu_options,
            font=enums.INVENTORY_FONT,
            empty_menu_message='Empty Inventory')
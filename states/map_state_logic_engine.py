from entities.entity import Entity
from systems.logger import Logger
from systems.IO import IO
from systems.time import Time
from entities.game_world import Game_World
import enums

DEFAULT_STATE = 'DEFAULT_STATE'
DROP_ITEM_STATE = 'DROP_ITEM_STATE'
EAT_ITEM_STATE = 'SHOWING_EDIBLE_ITEMS_STATE'
PICK_ITEM_STATE = 'PICK_ITEM_STATE'


class MapStateLogicEngine(object):
    def __init__(self, map_state):
        self.current_state = DEFAULT_STATE
        self.parent = map_state
        self.event = None
        self.actions = {
            # DIRECTIONS
            'left': self._direction,
            'right': self._direction,
            'up': self._direction,
            'down': self._direction,
            'descend': self._descend,
            # CHOOSE
            'drop item': self._choose_to_drop,
            'eat item': self._choose_to_eat,
            'show inventory': self._show_inventory,
            'pick up item': self._pick_item,
            'target': self._target,
            'quit': self._quit,
        }

    def run(self):
        ticks = 0
        messages = []
        message = None
        s = self.current_state
        if s == DROP_ITEM_STATE:
            item = self.parent.parameters.get("selected_item", None)
            self.current_state = DEFAULT_STATE
            if item:
                ticks, message = Entity.player.drop(item)
        elif s == EAT_ITEM_STATE:
            item = self.parent.parameters.get("selected_item", None)
            self.current_state = DEFAULT_STATE
            if item:
                ticks, message = Entity.player.consume(item)
        elif s == DEFAULT_STATE:
            self.event = self.parent.get_event()
            if self.event:
                ticks, message = self.actions[self.event]()

        messages.append(message)
        if ticks:
            turn_messages, game_over, game_over_message = Time.new_turn()
            messages.append(turn_messages)
            if game_over:
                Logger.game_over_message = game_over_message
                self.parent.next_game_state = enums.GAME_OVER_STATE
        if message:
            Logger.add_message(message)

    def _direction(self):
        target_tile = Game_World.dungeon.get_neighbor_tile(Entity.player.tile, self.event)
        if not target_tile or 'movement blocking' in target_tile.properties:
            return self._invalid_action()
        elif target_tile.tip == 'closed door':
            return Entity.player.open_door(target_tile)
        elif target_tile.container.get(properties='NPC'):
            NPC = target_tile.container.get(properties='NPC')
            return Entity.player.attack_to(NPC)
        else:
            return Entity.player.move(target_tile)

        #todo: close door

    def _descend(self):
        if Entity.player.tile.tip == 'exit':
            Logger.game_over_message = 'Congratulations. You found the way out.'
            self.parent.next_game_state = enums.GAME_OVER_STATE
        return 0, None

    def _show_inventory(self):
        self.parent.next_game_parameters = dict(inventory_key='')
        self.parent.next_game_state = enums.INVENTORY_STATE
        return 0, None

    def _pick_item(self):
        ticks = 0
        message = None
        items = [item for item in Entity.player.tile.container if 'pickable' in item.properties]
        if len(items) == 0:
            return ticks, message
        elif len(items) == 1:
            item = items[0]
            return Entity.player.pick(item)
        elif len(items) > 1:
            self._choose_item_from_inventory('')
            self.current_state = 'pick up item'
        return ticks, message

    def _choose_to_drop(self):
        self._choose_item_from_inventory('')
        self.current_state = DROP_ITEM_STATE
        IO.set_active_event('pass')
        return 0, None

    def _choose_to_eat(self):
        self._choose_item_from_inventory('edible')
        self.current_state = EAT_ITEM_STATE
        IO.set_active_event('pass')
        return 0, None

    def _target(self):
        self.parent.next_game_state = enums.TARGETING_STATE
        return 0, None

    def _quit(self):
        self.parent.next_game_state = enums.MAIN_MENU_STATE
        return 0, None

    def _invalid_action(self):
        IO.set_active_event(None)
        return 0, None

    def _choose_item_from_inventory(self, key):
        self.parent.next_game_state_parameters = dict(inventory_key=key,
                                                      state='CHOOSING_ITEM_FROM_MAP_STATE')
        self.parent.next_game_state = enums.INVENTORY_STATE

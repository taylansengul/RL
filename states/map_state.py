import base_state
from entities.entity import Entity
from entities.game_world import Game_World
import enums
from systems import draw
from systems.IO import IO
from systems.logger import Logger
from systems.time import Time

DEFAULT_STATE = 'DEFAULT_STATE'
DROP_ITEM_STATE = 'DROP_ITEM_STATE'
EAT_ITEM_STATE = 'EAT_ITEM_STATE'
PICK_ITEM_STATE = 'PICK_ITEM_STATE'


class MapState(base_state.BaseState):

    def __init__(self):
        super(MapState, self).__init__(enums.MAP_STATE)
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
            None: lambda: (0, "")
        }
        self.current_state = DEFAULT_STATE
        self.incoming_keys = ['selected_inventory_item']
        self.selected_inventory_item = None
        self.event = None

    def init(self):
        super(MapState, self).init()
        self.update_screen()

    def determine_action(self):
        super(MapState, self).determine_action()
        messages = []
        if self.current_state != DEFAULT_STATE:
            ticks, message = self.non_default_state_actions()
        else:
            self.event = self.get_event()
            ticks, message = self.actions[self.event]()

        self.current_state = DEFAULT_STATE
        self.selected_inventory_item = None

        print 'map state determine action 1', message
        if message:
            messages.append(message)
        if ticks:
            turn_messages, game_over, game_over_message = self.process_ticks()
        else:
            turn_messages, game_over, game_over_message = [], False, ""

        if turn_messages:
            print 'map state determine action 2', turn_messages
            messages.append(turn_messages)
        if game_over:
            Logger.game_over_message = game_over_message
            self.next_game_state = enums.GAME_OVER_STATE
        if messages:
            Logger.add(messages)

    @staticmethod
    def process_ticks():
        return Time.new_turn()

    def non_default_state_actions(self):
        ticks, message = 0, None
        item = self.selected_inventory_item
        if self.current_state == DROP_ITEM_STATE and item:
            ticks, message = Entity.player.drop(item)
        elif self.current_state == EAT_ITEM_STATE and item:
            ticks, message = Entity.player.consume(item)
        return ticks, message

    def update_screen(self):
        draw.clear_all_screens()
        draw.dungeon(Entity.player, enums.MAP_SCREEN)
        draw.messages_screen()
        draw.player_stats(Entity.player)
        draw.render_turn(Time.turn, enums.GAME_INFO_SCREEN)
        draw.update()

    def _direction(self):
        # todo: close door
        target_tile = Game_World.dungeon.get_neighbor_tile(Entity.player.tile, self.event)
        if not target_tile or 'movement blocking' in target_tile.properties:
            return self._invalid_action()
        elif target_tile.tip == 'closed door':
            return Entity.player.open_door(target_tile)
        elif target_tile.container.get(properties='NPC'):
            npc = target_tile.container.get(properties='NPC')
            return Entity.player.attack_to(npc)
        else:
            return Entity.player.move(target_tile)

    def _descend(self):
        if Entity.player.tile.tip == 'exit':
            Logger.game_over_message = 'Congratulations. You found the way out.'
            self.next_game_state = enums.GAME_OVER_STATE
        return 0, None

    def _show_inventory(self):
        self.outgoing = dict(key='')
        self.next_game_state = enums.INVENTORY_STATE
        return 0, None

    def _pick_item(self):
        ticks = 0
        message = None
        items = [
            item for item in Entity.player.tile.container if 'pickable' in item.properties]
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
        self.next_game_state = enums.TARGETING_STATE
        return 0, None

    def _quit(self):
        self.next_game_state = enums.MAIN_MENU_STATE
        return 0, None

    @staticmethod
    def _invalid_action():
        IO.set_active_event(None)
        return 0, None

    def _choose_item_from_inventory(self, key):
        self.outgoing = dict(key=key,
                             current_state='CHOOSING_ITEM_FROM_MAP_STATE')
        self.next_game_state = enums.INVENTORY_STATE

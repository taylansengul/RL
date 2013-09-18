from entities.entity import Entity
from systems.logger import Logger
from systems.IO import IO

DEFAULT_STATE = 'DEFAULT_STATE'
DROP_ITEM_STATE = 'DROP_ITEM_STATE'
EAT_ITEM_STATE = 'SHOW_EDIBLE_ITEMS_STATE'
PICK_ITEM_STATE = 'PICK_ITEM_STATE'


class MapStateLogicEngine(object):
    def __init__(self, game):
        self.game = game
        self.current_state = DEFAULT_STATE
        self.actions = {
            None: self._none,
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
        ticks, message = 0, None
        S = self.current_state
        if S == DROP_ITEM_STATE:
            item = self.game.inventory_state.selected_item
            self.current_state = DEFAULT_STATE
            ticks, message = Entity.player.drop(item)
        elif S == EAT_ITEM_STATE:
            item = self.game.inventory_state.selected_item
            self.current_state = DEFAULT_STATE
            ticks, message = Entity.player.consume(item)
        elif S == DEFAULT_STATE:
            self.event = IO.get_active_event()
            self.game.event_log.append(self.event)
            ticks, message = self.actions[self.event]()

        if ticks:
            self.game.time.new_turn()
        if message:
            Logger.add_message(message)

    def _none(self):
        print 'Why None event'
        return 0, None

    def _direction(self):
        print Entity.player, Entity.player.tile
        target_tile = self.game.game_world.dungeon.get_neighbor_tile(Entity.player.tile, self.event)
        if not target_tile or 'movement blocking' in target_tile.properties:
            return self._invalid_action()
        elif self.game.event_log[-2] == 'close door':
            return self._close_door(target_tile)
        elif target_tile.tip == 'closed door':
            return self._open_door(target_tile)
        elif target_tile.container.get(properties='NPC'):
            return self._attack(target_tile)
        else:
            return self._move(target_tile)

    def _attack(self, target_tile):
        NPC = target_tile.container[0]
        Entity.player.attack_to(NPC)
        NPC.attack_to(Entity.player)
        return 1

    def _move(self, target_tile):
        return Entity.player.move(target_tile)

    def _open_door(self, door_tile):
        return Entity.player.open_door(door_tile)

    def _close_door(self, door_tile):
        return Entity.player.close_door(door_tile)

    def _descend(self):
        if Entity.player.tile.tip == 'exit':
            Logger.game_over_message = 'Congratulations. You found the way out.'
            self.game.change_state(self.game.game_over_screen_state)
        return 0, None

    def _show_inventory(self):
        self.game.inventory_state.key = ''
        self.game.change_state(self.game.inventory_state)
        return 0, None

    def _pick_item(self):
        ticks = 0
        message = None
        C = Entity.player.tile.container
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
        self.game.change_state(self.game.targeting_state)
        return 0, None

    def _quit(self):
        self.game.change_state(self.game.main_menu_state)
        return 0, None

    def _invalid_action(self):
        IO.set_active_event(None)
        return 0, None

    def _choose_item_from_inventory(self, key):
        self.game.inventory_state.key = key
        self.game.inventory_state.current_state = 'CHOOSING_ITEM_FROM_MAP_STATE'
        self.game.change_state(self.game.inventory_state)
from objects.entity import Entity
from systems.logger import Logger
from systems.IO import IO


class MapStateLogicEngine(object):
    def __init__(self, game):
        self.game = game
        self.actions = {
            None: self._none,
            'up': self._direction,
            'down': self._direction,
            'left': self._direction,
            'right': self._direction,
            'descend': self._descend,
            'inventory_objects_list': self._show_inventory,
            'eat item': self._eat_item,
            'pick up item': self._pick_item,
            'drop item': self._drop_item,
            'target': self._target,
            'quit': self._quit,
        }

    def run(self):
        self.event = IO.get_active_event()
        self.game.event_log.append(self.event)
        self.player = Entity.player
        self.tile = self.player.tile
        ticks = self.actions[self.event]()
        if ticks:
            self.game.time.new_turn()

    def _none(self):
        print 'Why None event'
        return 0

    def _direction(self):
        target_tile = self.game.game_world.dungeon.get_neighbor_tile(self.tile, self.event)
        if not target_tile or 'movement blocking' in target_tile.properties:
            return self._invalid_action()
        elif self.game.event_log[-2] == 'close door':
            return self._close_door(target_tile)
        elif target_tile.tip == 'closed door':
            return self._open_door(target_tile)
        elif target_tile.container.lookup(dict(properties='NPC')):
            return self._attack(target_tile)
        else:
            return self._move(target_tile)

    def _attack(self, target_tile):
        NPC = target_tile.container[0]
        self.player.attack_to(NPC)
        NPC.attack_to(self.player)
        return 1

    def _move(self, target_tile):
        ticks = self.player.move(target_tile)
        return ticks

    def _open_door(self, door_tile):
        return self.player.open_door(door_tile)

    def _close_door(self, door_tile):
        return self.player.close_door(door_tile)

    def _descend(self):
        if self.tile.tip == 'exit':
            Logger.game_over_message = 'Congratulations. You found the way out.'
            self.game.change_state(self.game.game_over_screen_state)
        return 0

    def _show_inventory(self):
        self.game.inventory_state.key = ''
        self.game.change_state(self.game.inventory_state)
        return 0

    def _eat_item(self):
        self.game.inventory_state.key = 'edible'
        self.game.change_state(self.game.inventory_state)
        item = self.game.inventory_state.selected_item
        if item:
            return self.player.consume(item)
        else:
            return 0

    def _pick_item(self):
        if not self.tile.container.is_empty():
            for item in self.tile.container:
                if 'pickable' in item.properties:
                    self.tile.container.remove(item)
                    self.player.container.add(item)
                    item.tile = self.player.tile
                    return 1

    def _drop_item(self):
        if not self.player.container.is_empty():
            item = self.player.container[0]
            self.player.container.transfer_to(self.tile, item)
            return 1

    def _target(self):
        self.game.change_state(self.game.targeting_state)
        return 0

    def _quit(self):
        self.game.change_state(self.game.main_menu_state)
        return 0

    def _invalid_action(self):
        IO.set_active_event(None)
        return 0
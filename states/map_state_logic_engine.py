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
        ticks, message = self.actions[self.event]()
        if ticks:
            self.game.time.new_turn()
        if message:
            Logger.add_message(message)

    def _none(self):
        print 'Why None event'
        return 0

    def _direction(self):
        print Entity.player, Entity.player.tile
        target_tile = self.game.game_world.dungeon.get_neighbor_tile(Entity.player.tile, self.event)
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

    def _eat_item(self):
        self.game.inventory_state.key = 'edible'
        self.game.change_state(self.game.inventory_state)
        item = self.game.inventory_state.selected_item
        if item:
            return Entity.player.consume(item)
        else:
            return 0

    def _pick_item(self):
        ticks = 0
        message = None
        for item in Entity.player.tile.container:
            if 'pickable' in item.properties:
                Entity.player.tile.container.remove(item)
                Entity.player.container.add(item)
                item.tile = Entity.player.tile
                message = 'You picked up %s' % item.ID
                break
        return ticks, message

    def _drop_item(self):
        ticks = 0
        message = None
        if not Entity.player.container.is_empty():
            item = Entity.player.container[0]
            Entity.player.container.remove(item)
            Entity.player.tile.container.add(item)

            message = 'You dropped %s' % item.ID
        return ticks, message

    def _target(self):
        self.game.change_state(self.game.targeting_state)
        return 0, None

    def _quit(self):
        self.game.change_state(self.game.main_menu_state)
        return 0, None

    def _invalid_action(self):
        IO.set_active_event(None)
        return 0, None
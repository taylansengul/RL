from objects.entity import Entity


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
        self.event = self.game.io_handler.get_active_event()
        self.game.event_log.append(self.event)
        self.player = Entity.player
        self.tile = self.player.tile
        self.actions[self.event]()

    def _none(self):
        print 'Why None event'
        pass

    def _direction(self):
        target_tile = self.game.game_world.dungeon.get_neighbor_tile(self.tile, self.event)
        if not target_tile or 'movement blocking' in target_tile.properties:
            self._invalid_action()
        elif self.game.event_log[-2] == 'close door':
            self._close_door(target_tile)
        elif target_tile.tip == 'closed door':
            self._open_door(target_tile)
        elif target_tile.container.lookup(dict(properties='NPC')):
            self._attack(target_tile)
        else:
            self._move(target_tile)

    def _attack(self, target_tile):
        NPC = target_tile.container[0]
        self.player.attack_to(NPC)
        NPC.attack_to(self.player)

    def _move(self, target_tile):
        self.player.move(target_tile)

    def _open_door(self, door_tile):
        self.player.open_door(door_tile)

    def _close_door(self, door_tile):
        self.player.close_door(door_tile)

    def _descend(self):
        if self.tile.tip == 'exit':
            self.game.logger.game_over_message = 'Congratulations. You found the way out.'
            self.game.change_state(self.game.game_over_screen_state)

    def _show_inventory(self):
        self.game.inventory_state.key = ''
        self.game.change_state(self.game.inventory_state)

    def _eat_item(self):
        self.game.inventory_state.key = 'edible'
        self.game.change_state(self.game.inventory_state)
        item = self.game.inventory_state.selected_item
        if item:
            self.player.consume(item)

    def _pick_item(self):
        if not self.tile.container.is_empty():
            for item in self.tile.container:
                if 'pickable' in item.properties:
                    self.tile.container.remove(item)
                    self.player.container.add(item)
                    item.tile = self.player.tile
                    break

    def _drop_item(self):
        if not self.player.container.is_empty():
            item = self.player.container[0]
            self.player.container.transfer_to(self.tile, item)

    def _target(self):
        self.game.change_state(self.game.targeting_state)

    def _quit(self):
        self.game.change_state(self.game.main_menu_state)

    def _invalid_action(self):
        self.game.io_handler.set_active_event(None)
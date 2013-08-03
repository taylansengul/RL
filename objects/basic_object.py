from data import Colors, game_items
from rechargeable import Rechargeable


class Game_Object(object):
    def __init__(self, game, **kwargs):
        self.game = game
        self.name = kwargs['name']
        self.coordinates = kwargs['coordinates']
        self.icon = kwargs['icon']
        self.color = Colors.palette[kwargs['color']]
        self.properties = kwargs.get('properties', '')
        self.effects = kwargs.get('effects', {})
        if 'has inventory' in self.properties:
            self.objects = []
            for name in kwargs.get('objects', []):
                pass
        if 'is alive' in self.properties:
            self.is_alive = True
            self.hp = Rechargeable(capacity=kwargs['hp'])
        if 'stackable' in self.properties:
            self.quantity = kwargs.get('quantity', 1)

        # add self to game objects
        self.game.objects_handler.all_objects.append(self)

    # OBJECTS HANDLING
    # ---- start -----
    def get_item_by_name(self, name):
        for item in self.objects:
            if item.name == name:
                return item
        else:
            return None

    def add_object(self, item):
        assert 'has inventory' in self.properties  # only applies if self has inventory
        self.objects.append(item)

    def remove_object(self, item):
        assert 'has inventory' in self.properties and item in self.objects
        self.objects.remove(item)

    def consume(self, item):
        assert 'consumable' in item.properties
        for effect in item.effects:
            if effect['type'] == 'satiate hunger':
                self.hunger.change_current(effect['amount'])
                self.remove_object(item)

    def transfer_to(self, other, item):
        self.remove_object(item)
        other.add_object(item)

    def has_objects(self):
        return self.objects != []

    def get_objects_info(self):
        return str(self.objects)
    #----- end ------

    # MOVEMENT HANDLING
    #----- start ------
    def move(self, tile):
        if 'movable' not in self.properties:
            return False
        elif 'blocks movement' in tile.properties:
            return False
        else:  # if the target tile is a valid tile.
            # move
            self.game.game_world.change_position_of(self, tile.coordinates)
            return True

    def open_door(self, tile):
        if 'can open doors' in self.properties:  # self can open doors
            tile.set_tip('open door')
            self.game.logger.add_message('A door has been opened.')
            return True
        else:
            return False
    #----- end -----
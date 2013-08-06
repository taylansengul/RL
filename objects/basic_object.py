import data
from rechargeable import Rechargeable


class Game_Object(object):
    def __init__(self, game, **kwargs):
        self.game = game
        self.id = kwargs['id']
        self.coordinates = kwargs['coordinates']
        self.icon = kwargs['icon']
        self.color = data.colors.palette[kwargs['color']]
        self.properties = kwargs.get('properties', '')
        self.effects = kwargs.get('effects', {})
        if 'has inventory' in self.properties:
            self.objects = []
            for id in kwargs.get('objects', []):
                pass
        if 'stackable' in self.properties:
            self.quantity = kwargs.get('quantity', 1)
        if 'NPC' in self.properties or 'player' in self.properties:
            self.attack = kwargs['attack']
            self.defense = kwargs['defense']
            self.hp = Rechargeable(capacity=kwargs['hp'])
            self.is_alive = True
        if 'player' in self.properties:
            self.hunger = Rechargeable(capacity=100)
            self.money = 1000
            self.visibility_radius = 2

        # add self to game objects
        self.game.objects_handler.all_objects.append(self)

    # OBJECTS HANDLING
    # ---- start -----
    def get_item_by_id(self, id):
        for item in self.objects:
            if item.id == id:
                return item
        else:
            return None

    def add_object(self, item):
        assert 'has inventory' in self.properties  # only applies if self has inventory
        self_item = self.get_item_by_id(item.id)
        if 'stackable' in item.properties:
            if self_item:
                self_item.quantity += 1
            else:
                self_item = Game_Object(self.game, coordinates=self.coordinates, **data.game_items.dictionary[item.id])
                self.objects.append(self_item)
        else:
            self.objects.append(item)

    def remove_object(self, item):
        assert 'has inventory' in self.properties and item in self.objects
        self.objects.remove(item)

    def add_object(self, item):
        assert 'has inventory' in self.properties  # only applies if self has inventory
        if 'stackable' in item.properties:
            # add item
            self_item = self.get_item_by_id(item.id)
            if self_item:  # if self has the item
                self_item.quantity += 1  # increase quanitity
            else:
                new_item = Game_Object(self.game, coordinates=self.coordinates, **data.game_items.dictionary[item.id])
                self.game.objects_handler.add_game_item(new_item, self)  # create and add item
        else:  # if item is not stackable
            self.objects.append(item)

    def remove_object(self, item):
        assert 'has inventory' in self.properties and item in self.objects
        # remove item
        if 'stackable' in item.properties:
            if item.quantity > 1:       # if more than 1
                item.quantity -= 1      # decrease quantity
            elif item.quantity == 1:    # if 1
                self.game.objects_handler.remove_game_item(item, self)  # destroy and remove item
        else:
            self.objects.remove(item)

    def transfer_to(self, other, item):
        self.remove_object(item)  # remove item from inventory
        other.add_object(item)

    def consume(self, item):
        assert 'consumable' in item.properties
        for effect in item.effects:
            if effect['type'] == 'satiate hunger':
                self.hunger.change_current(effect['amount'])
                self.remove_object(item)
            if effect['type'] == 'heal':
                self.hp.change_current(effect['amount'])
                self.remove_object(item)

    def has_an_object_which_is(self, a_property):
        if self.has_objects():
            for an_object in self.objects:
                if a_property in an_object.properties:
                    return True
            else:
                return False

    def has_objects(self):
        return self.objects != []

    def get_objects_info(self):
        return str(self.objects)

    def get_objects(self, key):
        return_list = []
        for item in self.objects:
            if key in item.properties:
                return_list.append(item)
        return return_list
    #----- end ------

    # MOVEMENT HANDLING
    #----- start ------
    def move(self, tile):
        b1 = 'movable' in self.properties
        b2 = not 'movement blocking' in tile.properties
        b3 = not tile.has_an_object_which_is('movement blocking')

        if b1 and b2 and b3 and b3:
            self.game.game_world.change_position_of(self, tile.coordinates)
            self.game.time.new_turn()

    def open_door(self, tile):
        if 'can open doors' in self.properties:  # self can open doors
            tile.set_tip('open door')
            self.game.logger.add_message('A door has been opened.')
            return True
        else:
            return False
    #----- end -----

    # ATTACK - TAKE HIT - DIE
    # ---- start ----

    def attack_to(self, other):
        damage = max(self.attack - other.defense, 0)
        other.take_hit(damage)

    def take_hit(self, damage):
        self.hp.change_current(-damage)
        self.update_status()

    def update_status(self):
        assert 'NPC' in self.properties or 'player' in self.properties
        # hit points
        if self.hp.is_zero():
            self.is_alive = False
            if 'player' in self.properties:
                self.game.logger.game_over_message = 'You died of bleeding.'
        # is self dead
        if 'NPC' in self.properties:
            if not self.is_alive:
                tile = self.game.game_world.get_tile(self.coordinates)
                self.game.objects_handler.remove_NPC(self, tile)
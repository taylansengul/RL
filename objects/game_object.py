from rechargeable import Rechargeable
from graphics.text import Text


class Game_Object(object):
    def __init__(self, game, **kwargs):
        self.game = game
        self.ID = kwargs['ID']
        self.tile = kwargs.get('tile', self)  # if no tile it must be a tile and hence it points to itself
        self.icon = kwargs['icon']
        self.color = self.game.data.colors.palette[kwargs['color']]
        self.properties = kwargs.get('properties', '')
        self.effects = kwargs.get('effects', {})
        self.description = kwargs.get('description', '')
        if 'container' in self.properties:
            self.objects = []
            for ID in kwargs.get('objects', []):  # creating self.objects from string list
                item_kwargs = self.game.data.game_items.dictionary[ID]
                new_item = Game_Object(self.game, tile=self.tile, **item_kwargs)
                self.game.objects_handler.add_game_item(new_item, self)
        if 'stackable' in self.properties:
            self.quantity = kwargs.get('quantity', 1)
        if 'NPC' in self.properties or 'player' in self.properties:
            self.attack = kwargs['attack']
            self.defense = kwargs['defense']
            self.hp = Rechargeable(self.game, owner=self, capacity=kwargs['hp'])
            self.is_alive = True
            self.current_conditions = kwargs.get('conditions', '')
        if 'player' in self.properties:
            self.hunger = Rechargeable(self.game, owner=self, capacity=100)
            for condition in kwargs.get('conditions', []):  # if there are conditions
                getattr(self, condition['effects']).add_condition(condition)
            self.money = 1000
            self.visibility_radius = kwargs['visibility radius']

        # add self to game objects
        self.game.objects_handler.all_objects.append(self)

    # OBJECTS HANDLING
    # ---- start -----
    def get_item_by_id(self, ID):
        for item in self.objects:
            if item.ID == ID:
                return item
        else:
            return None

    def add_object(self, item):
        assert 'container' in self.properties  # only applies if self container
        item.tile = self.tile
        if 'stackable' in item.properties:
            # add item
            self_item = self.get_item_by_id(item.ID)
            if self_item:  # if self has the item
                self_item.quantity += 1  # increase quantity
            else:
                new_item = Game_Object(self.game, tile=self.tile, **self.game.data.game_items.dictionary[item.ID])
                self.game.objects_handler.add_game_item(new_item, self)  # create and add item
        else:  # if item is not stackable
            self.objects.append(item)

    def remove_object(self, item):
        assert 'container' in self.properties and item in self.objects
        item.tile = None
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
        for condition in item.effects:
            getattr(self, condition['effects']).add_condition(condition)
        self.remove_object(item)
        self.game.time.new_turn()

    def has_an_object_which_is(self, a_property):
        if self.has_objects():
            for an_object in self.objects:
                if a_property in an_object.properties:
                    return True
            else:
                return False

    def has_objects(self):
        return self.objects != []

    def get_objects(self, key):
        return_list = []
        for item in self.objects:
            if key in item.properties:
                return_list.append(item)
        return return_list

    @staticmethod
    def get_condition(key, search_string):
        term = key+'('
        start = search_string.find(term) + len(term)
        end = search_string.find(')', start)
        return search_string[start: end]

    @staticmethod
    def remove_condition(key, search_string):
        start = search_string.find(key)
        end = search_string.find(')', start)
        if end == len(search_string):
            new = search_string[:start]
        else:
            new = search_string[:start] + search_string[end+1:]
        return new

    @staticmethod
    def add_condition(key, search_string):
        if search_string == '':
            search_string = key
        else:
            search_string = search_string + ', ' + key
        return search_string
    #----- end ------

    # MOVEMENT HANDLING
    #----- start ------
    def move(self, target_tile):
        b1 = 'movable' in self.properties
        b2 = not 'movement blocking' in target_tile.properties
        b3 = not target_tile.has_an_object_which_is('movement blocking')

        if b1 and b2 and b3 and b3:
            self.tile.transfer_to(target_tile, self)
            self.game.time.new_turn()

    def open_door(self, target_tile):
        if target_tile.tip != 'open door':
            return False
        if 'can open doors' in self.properties:
            target_tile.set_tip('open door')
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
        if self.hp.is_zero():
            self.is_alive = False
            if 'player' in self.properties:
                self.game.logger.game_over_message = 'You died of bleeding.'
        # is self dead
        if 'NPC' in self.properties:
            if not self.is_alive:
                self.game.objects_handler.remove_NPC(self, self.tile)

    def render_icon_to(self, screen):
        t = Text(screen=screen,
                 font='map object',
                 context=self.icon,
                 coordinates=self.tile.screen_position,
                 color=self.color,
                 horizontal_align='center',
                 vertical_align='center')
        t.render()

    def render_description_to(self, screen):
        screen.clear()
        context = self.description
        t = Text(font='inventory', screen=screen, context=context, coordinates=(0, 0), color='white')
        t.render()
        screen.render()

    @property
    def inventory_repr(self):
        if 'stackable' in self.properties:
            return str(self.quantity) + ' ' + self.ID
        else:
            return self.ID
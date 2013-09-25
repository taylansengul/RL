from resource import Resource
import container
import copy


class Entity(object):
    all_NPCs = []
    all_things = []
    player = None

    @staticmethod
    def add_new(entity):
        P = entity.properties
        if 'NPC' in P:
            Entity.all_NPCs.append(entity)
        elif 'thing' in P:
            Entity.all_things.append(entity)
        elif 'player' in P:
            Entity.player = entity

    @staticmethod
    def remove_old(entity):
        P = entity.properties
        if 'NPC' in P:
            Entity.all_NPCs.remove(entity)
        elif 'thing' in P:
            Entity.all_things.remove(entity)
        elif 'player' in P:
            Entity.player = None

    @staticmethod
    def erase_all_entities():
        Entity.all_NPCs = []
        Entity.all_things = []
        Entity.player = None

    def __init__(self, **kwargs):
        self.ID = kwargs.get('ID', None)
        self.properties = kwargs.get('properties', '')
        if 'tile' in self.properties:
            self.tile = self
        else:
            self.tile = kwargs.get('tile', None)
        if 'container' in self.properties:
            self.container = container.Container()
        if 'stackable' in self.properties:
            self.quantity = kwargs.get('quantity', 1)
        if 'NPC' in self.properties or 'player' in self.properties:
            self.attack = kwargs.get('attack', None)
            self.defense = kwargs.get('defense', None)
        if 'alive' in self.properties:
            self.hp = Resource(maximum=kwargs['hp'])
            self.is_alive = True
        if 'player' in self.properties:
            self.name = 'George'
        if 'needs food' in self.properties:
            self.hunger = Resource(maximum=kwargs['hunger'])
        if 'has vision' in self.properties:
            self.visibility_radius = kwargs['visibility radius']
        if 'drawable' in self.properties:
            self.icon = kwargs.get('icon', '?')
            self.description = kwargs.get('description', '')
            self.color = kwargs.get('color', None)
            self.image = kwargs.get('image', None)
        if 'equipable' in self.properties:
            self.equipped = False
        if 'consumable' in self.properties:
            self.effects = kwargs.get('effects', {})

        for condition in kwargs.get('conditions', []):
            self.add_condition(condition)

        Entity.add_new(self)

    # OBJECTS HANDLING
    # ---- start -----
    def remove_tile(self):
        self.tile.container.rem(self)
        self.tile = None

    def set_tile(self, new_tile):
        new_tile.container.add(self)
        self.tile = new_tile

    def drop(self, item):
        # todo: move stackable into container
        ticks = 0
        message = None
        if item is None or item not in self.container:
            return ticks, message
        if 'stackable' in item.properties and item.quantity > 1:
            self.container.rem(item)
            new_item = copy.deepcopy(item)
            new_item.quantity = 1
            new_item.set_tile(self.tile)
        else:
            self.container.rem(item)
            item.set_tile(self.tile)
        message = 'You dropped %s' % item.ID
        return ticks, message

    def equip(self, item):
        ticks = 0
        message = None
        if 'equipable' in item.properties and not item.equipped:
            for condition in item.effects:
                self.add_condition(condition)
            item.equipped = True
            message = 'You put on %s.' % item.ID
            ticks = 1
        return ticks, message


    def pick(self, item):
        ticks = 1
        message = 'You picked up %s' % item.ID
        assert 'pickable' in item.properties
        item.remove_tile()
        self.container.add(item)
        return ticks, message

    def consume(self, item):
        assert 'consumable' in item.properties
        ticks = 1
        message = '%s consumed a %s' % (self.ID, item.ID)
        for condition in item.effects:
            self.add_condition(condition)
        self.container.rem(item)
        return ticks, message
    #----- end ------

    # CONDITIONS HANDLING
    def add_condition(self, condition):
        getattr(self, condition['resource']).add_condition(condition)

    # MOVEMENT HANDLING
    #----- start ------
    def move(self, target_tile):
        ticks = 0
        message = None
        b1 = 'movable' in self.properties
        b2 = not 'movement blocking' in target_tile.properties
        b3 = not target_tile.container.get(properties='movement blocking')

        if b1 and b2 and b3 and b3:
            self.tile.container.rem(self)
            target_tile.container.add(self)
            self.tile = target_tile
            ticks = 1
            message = 'Moved'
        return ticks, message

    def open_door(self, target_tile):
        ticks = 0
        message = None
        if 'can open doors' in self.properties and target_tile.tip == 'open door':
            target_tile.set_tip('open door')
            ticks = 1
            message = 'A door has been opened.'
        return ticks, message
    #----- end -----

    # ATTACK - TAKE HIT - DIE
    # ---- start ----
    def attack_to(self, other):
        ticks = 1
        message1 = self.hit(other)
        message2 = other.hit(self)
        message = message1 + ' ' + message2
        return ticks, message

    def hit(self, other):
        damage = max(self.attack - other.defense, 0)
        other.hp.change_current(-damage)
        message = '%s hit %s for %d damage.' % (self.ID, other.ID, damage)
        return message

    def update_status(self):
        assert 'NPC' in self.properties or 'player' in self.properties
        message = None
        game_over = False
        if 'needs food' in self.properties and self.hunger.less_than_minimum():
            self.is_alive = False
            message = '%s died of hunger.' % self.ID
        elif self.hp.less_than_minimum():
            self.is_alive = False
            message = '%s is dead.' % self.ID
        # is self dead
        if not self.is_alive:
            if 'NPC' in self.properties:
                self.remove_tile()
                Entity.remove_old(self)
            elif 'player' in self.properties:
                game_over = True

        return message, game_over

    @property
    def inventory_repr(self):
        if 'stackable' in self.properties:
            return str(self.quantity) + ' ' + self.ID
        else:
            return self.ID
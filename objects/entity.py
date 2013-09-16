from resource import Resource
from graphics.text import Text
from globals import *
import os
import data
import pygame
import container
from systems.logger import Logger


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

    def __init__(self, game, **kwargs):
        self.game = game
        self.ID = kwargs['ID']
        self.tile = kwargs.get('tile', self)  # if no tile it must be a tile and hence it points to itself
        self.icon = kwargs.get('icon', '?')
        self.color = ColorID[kwargs['color']]
        self.properties = kwargs.get('properties', '')
        self.effects = kwargs.get('effects', {})
        self.description = kwargs.get('description', '')
        if 'container' in self.properties:
            self.container = container.Container()
            for ID in kwargs.get('objects', []):  # creating self.objects from string list
                item_kwargs = data.game_items.dictionary[ID]
                new_item = Entity(self.game, tile=self.tile, **item_kwargs)
                self.container.add(new_item)
        if 'stackable' in self.properties:
            self.quantity = kwargs.get('quantity', 1)
        if 'NPC' in self.properties or 'player' in self.properties:
            self.attack = kwargs['attack']
            self.defense = kwargs['defense']
            self.hp = Resource(self.game, owner=self, maximum=kwargs['hp'])
            self.is_alive = True
            self.current_conditions = kwargs.get('conditions', '')
        if 'player' in self.properties:
            self.hunger = Resource(self.game, owner=self, maximum=100)
            for condition in kwargs.get('conditions', []):  # if there are conditions
                getattr(self, condition['effects']).add_condition(condition)
            self.money = 1000
            self.visibility_radius = kwargs['visibility radius']
            self.name = 'George'

        #todo: images
        if kwargs.get('image', None):
            image_location = os.path.join('images', kwargs['image'])
            self.image = pygame.image.load(image_location).convert_alpha()
        else:
            self.image = None

        Entity.add_new(self)

    # OBJECTS HANDLING
    # ---- start -----

    def consume(self, item):
        assert 'consumable' in item.properties
        for condition in item.effects:
            getattr(self, condition['effects']).add_condition(condition)
        self.container.remove(item)
        self.game.time.new_turn()

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
        b3 = not target_tile.container.lookup(dict(properties='movement blocking'))

        if b1 and b2 and b3 and b3:
            self.tile.container.remove(self)
            target_tile.container.add(self)
            self.tile = target_tile
            self.game.time.new_turn()
        Logger.add_message('Moved.')

    def open_door(self, target_tile):
        if target_tile.tip != 'open door':
            return False
        if 'can open doors' in self.properties:
            target_tile.set_tip('open door')
            Logger.add_message('A door has been opened.')
            return True
        else:
            return False
    #----- end -----

    # ATTACK - TAKE HIT - DIE
    # ---- start ----
    def attack_to(self, other):
        damage = max(self.attack - other.defense, 0)
        other.take_hit(damage)
        Logger.add_message('%s hit %s for %d damage.' % (self.ID, other.ID, damage))

    def take_hit(self, damage):
        self.hp.change_current(-damage)
        self.update_status()

    def update_status(self):
        assert 'NPC' in self.properties or 'player' in self.properties
        if self.hp.is_zero():
            self.is_alive = False
            if 'player' in self.properties:
                Logger.game_over_message = 'You died of bleeding.'
        # is self dead
        if 'NPC' in self.properties:
            if not self.is_alive:
                Logger.add_message('%s is dead.' % self.ID)
                self.tile.container.remove(self)
                Entity.remove_old(self)

    def render_icon_to(self, screen):
        if self.image:
            screen.surface.blit(self.image, self.tile.screen_position)
        else:
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
        t = Text(font=INVENTORY_FONT, screen=screen, context=context, coordinates=(0, 0), color='white')
        t.render()
        screen.render_to_main()

    @property
    def inventory_repr(self):
        if 'stackable' in self.properties:
            return str(self.quantity) + ' ' + self.ID
        else:
            return self.ID
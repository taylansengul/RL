from unittest import TestCase
from entities.entity import Entity


__author__ = 'Taylan Sengul'


class TestEntity(TestCase):
    def new_NPC(self):
        return Entity(ID='orc', properties='NPC')

    def new_container(self):
        return Entity(ID='backpack', properties='container')

    def new_thing(self):
        return Entity(properties='thing')

    def new_pickable_thing(self):
        return Entity(properties='pickable, thing')

    def new_tile(self):
        return Entity(ID='tile', properties='container')

    def new_player(self):
        return Entity(properties='player container', ID='player')

    def new_stackable_thing(self):
        return Entity(properties='thing stackable', ID='banana')

    def test_add_new(self):
        Entity.erase_all_entities()
        an_NPC = self.new_NPC()
        a_player = self.new_player()
        a_thing = self.new_thing()
        self.assertEquals(Entity.all_NPCs, [an_NPC])
        self.assertEquals(Entity.player, a_player)
        self.assertEquals(Entity.all_things, [a_thing])
        Entity.erase_all_entities()

    def test_remove_old(self):
        Entity.erase_all_entities()
        # add and remove an NPC
        an_NPC = self.new_NPC()
        self.assertNotEquals(Entity.all_NPCs, [])
        Entity.remove_old(an_NPC)
        self.assertEquals(Entity.all_NPCs, [])
        # add and remove a player
        a_player = self.new_player()
        self.assertNotEquals(Entity.player, None)
        Entity.remove_old(a_player)
        self.assertEquals(Entity.player, None)
        # add and remove an thing
        a_thing = self.new_thing()
        self.assertNotEquals(Entity.all_things, [])
        Entity.remove_old(a_thing)
        self.assertEquals(Entity.all_things, [])

    def test_reset(self):
        """
        1. create a new NPC, player, thing, 2.reset Entity class, 3. check if there is any entity stored in Entity
        """
        self.new_NPC()
        self.new_player()
        self.new_thing()
        Entity.erase_all_entities()
        self.assertEquals(Entity.all_NPCs, [])
        self.assertEquals(Entity.player, None)
        self.assertEquals(Entity.all_things, [])

    def test_drop(self):
        player = self.new_player()
        tile = self.new_tile()
        player.tile = tile
        tile.container.add(player)
        thing = self.new_thing()
        player.container.add(thing)
        self.assertEquals(player.container, [thing])
        player.drop(thing)
        self.assertEquals(player.container, [])
        self.assertEquals(player.tile.container, [player, thing])

    def test_pick(self):
        player = self.new_player()
        tile = self.new_tile()
        player.set_tile(tile)
        thing = self.new_pickable_thing()
        thing.set_tile(tile)
        self.assertEquals(player.container, [])
        player.pick(thing)
        self.assertEquals(player.container, [thing])
        self.assertEquals(player.tile.container, [player])
        self.assertEquals(player.tile, tile)
        self.assertEquals(thing.tile, None)
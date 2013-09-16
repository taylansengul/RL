from unittest import TestCase
from entities.container import Container
from entities.entity import Entity
__author__ = 'Taylan Sengul'


class TestContainer(TestCase):
    def new_container(self):
        return Container()

    def new_apple(self):
        return Entity(ID='apple', properties='edible')

    def new_medkit(self):
        return Entity(ID='medkit', properties='usable')

    def new_stackable(self):
        return Entity(ID='bullet', properties='stackable')

    def test_get(self):
        container = self.new_container()
        self.assertEquals(container.get(ID='medkit'), None)

    def test_get_1_add_1(self):
        apple = self.new_apple()
        container = self.new_container()
        container.add(apple)
        self.assertEquals(container.get(ID='apple'), apple)
        self.assertEquals(container.get(ID='medkit'), None)

    def test_get_1_add_2_different(self):
        apple = self.new_apple()
        medkit = self.new_medkit()
        container = self.new_container()
        container.add(apple)
        container.add(medkit)
        self.assertEquals(container.get(ID='apple'), apple)
        self.assertEquals(container.get(ID='medkit'), medkit)

    def test_get_all_add_2_same(self):
        apple1 = self.new_apple()
        apple2 = self.new_apple()
        container = self.new_container()
        container.add(apple1)
        container.add(apple2)
        # print container.get({'ID': 'apple'})
        self.assertEquals(container.get(key='all', ID='apple'), [apple1, apple2])

    def test_get_1_add_2_same(self):
        apple1 = self.new_apple()
        apple2 = self.new_apple()
        container = self.new_container()
        container.add(apple1)
        container.add(apple2)
        self.assertEquals(container.get(ID='apple'), apple1)

    def test_add_stackable1(self):
        a_stackable = self.new_stackable()
        container = self.new_container()
        container.add(a_stackable)
        self.assertEquals(container, [a_stackable])

    def test_add_stackable2(self):
        a_stackable1 = self.new_stackable()
        a_stackable2 = self.new_stackable()
        container = self.new_container()
        container.add(a_stackable1)
        container.add(a_stackable2)
        self.assertEquals(container, [a_stackable1])
        self.assertEquals(a_stackable1.quantity, 2)

    def test_add_two_item(self):
        apple1 = Entity(ID='apple', properties='edible red')
        apple2 = Entity(ID='apple', properties='edible yellow')
        container = self.new_container()
        container.add(apple1)
        container.add(apple2)
        self.assertEquals(container.get(properties='edible red'), apple1)
        self.assertEquals(container.get(properties='edible yellow'), apple2)
        self.assertEquals(container.get(properties='edible'), apple1)
        self.assertEquals(container.get(properties='edible', key='all'), [apple1, apple2])
        self.assertEquals(container.get(properties='red'), apple1)
        self.assertEquals(container.get(properties='yellow'), apple2)

    def test_remove_non_stackable1(self):
        apple = self.new_apple()
        container = self.new_container()
        container.add(apple)
        self.assertNotEquals(container, [])
        container.remove(apple)
        self.assertEquals(container, [])

    def test_remove_stackable1(self):
        a_stackable1 = self.new_stackable()
        container = self.new_container()
        container.add(a_stackable1)
        container.remove(a_stackable1)
        self.assertEquals(container, [])

    def test_remove_stackable2(self):
        a_stackable1 = self.new_stackable()
        a_stackable2 = self.new_stackable()
        container = self.new_container()
        container.add(a_stackable1)
        container.add(a_stackable2)
        container.remove(container.get(properties='stackable'))
        container.remove(container.get(properties='stackable'))
        self.assertEquals(container, [])

    def transfer(self):
        container1 = self.new_container()
        container2 = self.new_container()
        thing = self.new_apple()
        container1.add(thing)
        container1.transfer_to(container2, thing)
        self.assertEquals(container1, [])
        self.assertEquals(container2, [thing])
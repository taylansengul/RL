from unittest import TestCase
from entities.resource import Resource

__author__ = 'Taylan Sengul'


class TestResource(TestCase):
    def test_init(self):
        M = 10
        hp = Resource(maximum=M)
        self.assertEquals(hp.minimum, 0)
        self.assertEquals(hp.maximum, M)
        self.assertEquals(hp.current, M)

    def test_change_current(self):
        M = 10
        hp = Resource(maximum=M)
        hp.change_current(2)
        self.assertEquals(hp.minimum, 0)
        self.assertEquals(hp.maximum, M)
        self.assertEquals(hp.current, M)
        hp.change_current(-2)
        self.assertEquals(hp.minimum, 0)
        self.assertEquals(hp.maximum, M)
        self.assertEquals(hp.current, M-2)
        hp.change_current(1)
        self.assertEquals(hp.minimum, 0)
        self.assertEquals(hp.maximum, M)
        self.assertEquals(hp.current, M-1)

    def test_less_than_minimum(self):
        hp = Resource(maximum=10)
        self.assertFalse(hp.less_than_minimum())

    def test_add_condition(self):
        self.fail()
"""




    def test_remove_condition(self):
        self.fail()

    def test_update(self):
        self.fail()
"""
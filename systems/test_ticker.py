from unittest import TestCase
from time import Ticker
__author__ = 'Taylan Sengul'


class TestTicker(TestCase):

    class mock_object:
        def do_turn(self):
            pass

    def test_register(self):
        turn = 2
        obj = TestTicker.mock_object()
        Ticker.register(turn, obj)
        self.assertTrue(True)

    def test_get_tick(self):
        turn = 2
        obj = TestTicker.mock_object()
        self.assertEquals(None, Ticker.get_tick(obj))
        Ticker.register(turn, obj)
        self.assertEquals(turn, Ticker.get_tick(obj))

    def test_deregister(self):
        turn = 2
        obj = TestTicker.mock_object()
        self.assertEquals(None, Ticker.deregister(obj))
        Ticker.register(turn, obj)
        self.assertEquals(turn, Ticker.get_tick(obj))
        Ticker.deregister(obj)
        self.assertEquals(None, Ticker.get_tick(obj))

    def test_next_turn(self):
        turn = 2
        obj = TestTicker.mock_object()
        Ticker.register(turn, obj)
        for __ in range(turn+1):
            self.assertEquals(None, Ticker.next_turn())
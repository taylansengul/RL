from unittest import TestCase
from logger import Logger


__author__ = 'Taylan Sengul'


class TestLogger(TestCase):
    def test_add(self):
        cases = {"None": [],
                 "[None]": [],
                 "[None, '']": [],
                 "[None, '', [None, [None]]]": [],
                 "''": [],
                 "['as', 'bs']": ['as', 'bs']}
        for key in cases:
            Logger.unhandled_messages = []
            Logger.add(eval(key))
            self.assertEquals(Logger.unhandled_messages, cases[key])

    def test_add_multiple(self):
        Logger.unhandled_messages = []
        m1, m2, m3 = 'm1', 'm2', 'm3'
        Logger.add(m1, [m2, m3])
        self.assertEquals(Logger.unhandled_messages, [m1, m2, m3])

    def test_has_unhandled_messages(self):
        Logger.unhandled_messages = []
        self.assertFalse(Logger.has_unhandled_messages())
        Logger.add('messa')
        self.assertTrue(Logger.has_unhandled_messages())

    def test_handle_message(self):
        Logger.unhandled_messages = []
        Logger.archieve = []
        message = 'messa'
        Logger.add(message)
        self.assertEquals(Logger.unhandled_messages, [message])
        self.assertEquals(Logger.handle_message(), message)
        self.assertEquals(Logger.archieve, [message])
        self.assertEquals(Logger.unhandled_messages, [])
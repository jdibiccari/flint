import unittest
from flint.commands.utils import *

class TestConfigParser(unittest.TestCase):
    def test_parse(self):
        """It retrieves values from application ini file"""
        output = parse('database', 'migrations')
        self.assertEqual(output, 'db/migrations')

class TestConfigParser(unittest.TestCase):
    def test_get_message(self):
        """It retrieves a formatted message by key from a given dictionary of msgs"""
        TEST = {
        	'formatted_msg': 'This message contains a variable, foo = {foo}'
        }
        output = get_message(TEST, 'formatted_msg', {'foo': 'bar'})
        self.assertEqual(output, 'This message contains a variable, foo = bar')
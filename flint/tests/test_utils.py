import unittest
from flint.commands.utils import *

class TestNotification(unittest.TestCase):
    def test_get_message(self):
        """It retrieves a formatted message by key from a given dictionary of msgs"""
        TEST = {
            'formatted_msg': 'This message contains a variable, foo = {foo}'
        }
        output = get_message(TEST, 'formatted_msg', {'foo': 'bar'})
        self.assertEqual(output, 'This message contains a variable, foo = bar')

class TestValidation(unittest.TestCase):
    def test_validate_name_too_short(self):
        """It throws a validation error if name is too short"""
        with self.assertRaises(ValidationError):
            validate_name('Jan')

    def test_validate_name_too_long(self):
        """It throws a validation error if name is too long"""
        with self.assertRaises(ValidationError):
            validate_name('Janel-Lynn-diBiccari-First-of-Her-Name')

    def test_validate_name_not_alphanumeric(self):
        """It throws a validation error if name is not alphanumeric"""
        with self.assertRaises(ValidationError):
            validate_name('Janel&TheGang')

    def test_validate_name_ok(self):
        """It does not throw an error if name meets all criteria"""
        try:
            validate_name('Arya_Stark')
        except ExceptionType:
            self.fail("validate_name raised ValidationErro unexpectedly!")

    def test_validate_amount(self):
        pass

    def test_validate_credit_card(self):
        pass
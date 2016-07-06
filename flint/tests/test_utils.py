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
        """It throws a validation error if amount is less than 0"""
        with self.assertRaises(ValidationError):
            validate_amount(-500)

    def test_validate_credit_card_luhn_10_fail(self):
        """It throws a validation error if credit card fails luhn-10"""
        with self.assertRaises(ValidationError):
            validate_credit_card(1234567890123456)

    def test_validate_credit_card_luhn_10_success(self):
        """It doesn't raise error if card passes luhn-10"""
        try:
            validate_credit_card(5474942730093167)
        except ExceptionType:
            self.fail("validate_credit_card raised ValidationErro unexpectedly!")

    def test_is_luhn_compliant_success(self):
        """It returns true if card is luhn-10 compliant"""
        result = is_luhn_compliant(5227726754630966)
        self.assertTrue(result)

    def test_is_luhn_compliant_success(self):
        """It returns false if card is not luhn-10 compliant"""
        result = is_luhn_compliant(5227726754630963)
        self.assertFalse(result)
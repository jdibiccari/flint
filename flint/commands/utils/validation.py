import re
from notification import *

class ValidationError(Exception):
	def __init__(self, value, message):
		self.value = value
		self.message = message

def validate_name(name):
	err_msg = get_message(VALIDATION, 'invalid_name', {'name':name})
	if len(name) < 4 or len(name) > 20:
		raise ValidationError(name, err_msg)

	if not re.match('^[a-zA-Z0-9_\-]+$', name):
		raise ValidationError(name, err_msg)

def validate_amount(amount):
	err_msg = get_message(VALIDATION, 'invalid_amount')
	# Backing dollar amounts should accept both dollars and cents. Taken care of by click float arg type.
	if not amount >= 0:
		raise ValidationError(amount, err_msg)

def validate_credit_card(credit_card):
	err_msg = get_message(VALIDATION, 'invalid_card')
	# Credit card numbers will always be numeric. Taken care of by click arg type.
	# Credit card numbers may vary in length, up to 19 characters. Handled at database level.
	# Card numbers should be validated using Luhn-10
	if not is_luhn_compliant(credit_card):
		raise ValidationError(credit_card, err_msg)

# Reference: https://en.wikipedia.org/wiki/Luhn_algorithm
def is_luhn_compliant(credit_card):
	digits = list(map(int, str(credit_card)))
	odd_digits = digits[-1::-2]
	even_digits = digits[-2::-2]
	total = sum(odd_digits)
	for digit in even_digits:
		total += sum(divmod(2 * digit, 10))
	return total % 10 == 0


class ValidationError(Exception):
	def __init__(self, value, message):
		self.value = value
		self.message = message


def validate_name(name):
	if len(name) < 4 or len(name) > 20:
		raise ValidationError(name, 'ERROR: {} is not a valid name.'. format(name))


def validate_amount(amount):
	# Backing dollar amounts should accept both dollars and cents. Taken care of by click arg type.
	if not amount >= 0:
		raise ValidationError(amount, 'ERROR: Currency amounts must not be negative'. format(amount))

def validate_credit_card(credit_card):
	# Credit card numbers will always be numeric
	if not credit_card.isdigit():
		raise ValidationError(credit_card, 'ERROR: This card is invalid')

	# Card numbers should be validated using Luhn-10
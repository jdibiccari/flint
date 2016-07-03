import click
from utils.db_helpers import *
from utils.validators import *

@click.argument('amount', type=float)
@click.argument('credit_card', type=int)
@click.argument('project')
@click.argument('backer')
@click.command()
def back(backer, project, credit_card, amount):
	"""
	Back a project \n
	ex: back Mary Awesome_Sauce 5474942730093167 400
	"""
	# Validate inputs
	try:
		validate_name(backer)
		validate_name(project)
		validate_credit_card(credit_card)
	except ValidationError as e:
		click.echo(e.message)
		return

	# Does project already exist?
	art = find_by('projects', {'name': project})

	if not art:
		click.echo("ERROR: That project doesn't exist yet!")
		return

	patron = find_or_create('backers', {'name': backer})
	card = find_or_create('credit_cards', {'card_number': credit_card})

	if patron and card:
		project_id = art['id']
		backer_id = patron['id']
		card_id = card['id']

		# Try to link backer with credit card
		try:
			backer_card = create('backer_cards', {'credit_card_id': card_id, 'backer_id': backer_id})
		except sqlite3.IntegrityError:
			click.echo("ERROR: That card has already been added by another user!")
			return

		try:
			# Create the pledge linking backer and project
			create('pledges', {'backer_id': backer_id, 'project_id': project_id, 'amount': amount})
			# Update the project's amount_raised column
			update_amount_raised(project_id, amount)
		except sqlite3.IntegrityError:
			click.echo("ERROR: That backer has already backed this project!")
			return

		click.echo("{backer} backed project {project} for ${amount:.2f}".format(backer=backer, project=project, amount=amount))
	else:
		click.echo("Something went wrong.")


import click
from utils import *

# If any of the db interactions fail the others should probably be rolled back
@click.argument('amount', type=float)
@click.argument('credit_card', type=int)
@click.argument('project')
@click.argument('backer')
@click.command()
@pass_dbhandler
def back(dbhandler, backer, project, credit_card, amount):
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
		click.secho(e.message, fg='red')
		return

	# Does project already exist?
	prj = dbhandler.find_by('projects', {'name': project})

	if not prj:
		err_msg = get_message(BACK, 'project_not_found')
		warn(err_msg)
		return

	bckr = dbhandler.find_or_create('backers', {'name': backer})
	card = dbhandler.find_or_create('credit_cards', {'card_number': credit_card})

	project_id = prj['id']
	backer_id = bckr['id']
	card_id = card['id']

	# Try to link backer with credit card
	try:
		dbhandler.find_or_create('backer_cards', {'credit_card_id': card_id, 'backer_id': backer_id})
	except sqlite3.IntegrityError:
		err_msg = get_message(BACK, 'card_nonunique')
		warn(err_msg)
		return

	try:
		# Create the pledge linking backer and project
		dbhandler.create('pledges', {'backer_id': backer_id, 'project_id': project_id, 'amount': amount})
		# Update the project's amount_raised column
		dbhandler.update_amount_raised(project_id, amount)
	except sqlite3.IntegrityError:
		err_msg = get_message(BACK, 'backer_nonunique')
		warn(err_msg)
		return

	click.echo(get_message(BACK, 'success', {'backer': backer, 'project': project, 'amount':amount}))


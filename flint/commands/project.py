import click
from utils.db_helpers import *
from utils.validators import *

@click.argument('target_amount', type=float)
@click.argument('name')
@click.command()
def project(name, target_amount):
	"""
	Add a new project \n
	ex: project Galaxy_Guardians 800
	"""
	try:
		validate_name(name)
		validate_amount(target_amount)
	except ValidationError as e:
		click.echo(e.message)
		return

	try:
		create('projects', {'name': name, 'target_amount': target_amount})
	except sqlite3.IntegrityError:
		click.echo('ERROR: A project by that name already exists.')
		return

	click.echo ('Added {project} project with target of ${target}'.format(project=name, target=target_amount))
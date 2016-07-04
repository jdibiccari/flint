import click
import logging
from utils import *

@click.argument('target_amount', type=float)
@click.argument('name')
@click.command()
@pass_dbhandler
def project(dbhandler, name, target_amount):
	"""
	Add a new project \n
	ex: project Galaxy_Guardians 800
	"""
	try:
		validate_name(name)
		validate_amount(target_amount)
	except ValidationError as e:
		warn(e.message)
		return

	try:
		dbhandler.create('projects', {'name': name, 'target_amount': target_amount})
	except sqlite3.IntegrityError:
		err_msg = get_message(PROJECT, 'project_nonunique')
		log(__file__, err_msg)
		warn(err_msg)
		return

	click.echo(get_message(PROJECT, 'success', {'project': name, 'target': target_amount}))
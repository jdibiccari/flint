import click
from utils.db_handler import *

@click.command()
@pass_dbhandler
def reset(dbhandler):
	"""
	Resets your local database. Rolls back and re-applies migrations.
	"""
	if click.confirm(click.style('Do you want to reset your projects database?', fg='red')):
		notify('Resetting your project database...')
		dbhandler.reset_db()
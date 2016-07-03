import click
from utils.db_helpers import *

@click.command()
def reset():
	"""
	Resets your local database. Rolls back and re-applies migrations.
	"""
	if click.confirm('Do you want to reset your projects database?'):
		click.secho('Resetting your project database...', fg='red')
		reset_db()
import click
import os
from flint.commands.utils.db_helpers import setup_db, db_exists
from flint.commands import *

@click.group(invoke_without_command=True)
def flint():
	""" Flint:
	A light-weight, cli version of Kickstarter.
	"""
	if not db_exists():
		click.secho('Setting up your project database...', fg='green')
		setup_db()
	pass


flint.add_command(project.project)
flint.add_command(backer.backer)
flint.add_command(back.back)
flint.add_command(list.list)
flint.add_command(reset.reset)
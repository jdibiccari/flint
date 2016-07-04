import click
import os
from flint.commands.utils.db_handler import BaseDBHandler
from flint.commands import *

@click.group(invoke_without_command=True)
def flint():
	""" Flint:
	A light-weight, cli version of Kickstarter.
	"""
	if not BaseDBHandler.db_exists():
		click.secho('Setting up your project database...', fg='green')
		BaseDBHandler.setup_db()
	pass


flint.add_command(project.project)
flint.add_command(backer.backer)
flint.add_command(back.back)
flint.add_command(list.list)
flint.add_command(reset.reset)
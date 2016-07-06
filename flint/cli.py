import click
import logging
from flint.commands.utils import *
from flint.commands import *

@click.group(invoke_without_command=True)
@click.option('-t', '--test', default=False, is_flag=True, help='Run in test mode')
@pass_dbhandler
def flint(dbhandler, test):
	""" Flint:
	A light-weight, cli version of Kickstarter.
	"""

	if test:
		dbhandler.test_mode()

	if not dbhandler.db_exists():
		notify('Setting up your project database at {db_path}...'.format(db_path=dbhandler.db_path))
		dbhandler.setup_db()

flint.add_command(project)
flint.add_command(backer)
flint.add_command(back)
flint.add_command(list)
flint.add_command(reset)
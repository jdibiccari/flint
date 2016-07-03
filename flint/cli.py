import click
import os
import sqlite3
from ConfigParser import SafeConfigParser
from yoyo import read_migrations, get_backend
from flint.commands.back import *
from flint.commands.project import *
from flint.commands.backer import *
from flint.commands.list import *

# Move db logic to utils
parser = SafeConfigParser()
parser.read('flint_config.ini')
db = parser.get('database', 'db')
migration_directory = parser.get('database', 'migrations')

def get_db_migrations():
	backend = get_backend(db)
	migrations = read_migrations(migration_directory)
	return backend, migrations

def setup_db():
	backend, migrations = get_db_migrations()
	backend.apply_migrations(backend.to_apply(migrations))

def reset_db():
	backend, migrations = get_db_migrations()
	backend.rollback_migrations(backend.to_rollback(migrations))
	backend.apply_migrations(backend.to_apply(migrations))

@click.group(invoke_without_command=True)
def flint():
	""" Flint:
	A light-weight, cli version of Kickstarter.
	"""
	if not os.path.isfile('db/flint.sqlite'):
		click.secho('Setting up your project database...', fg='green')
		setup_db()
	pass

@click.command()
def reset():
	"""
	Resets your local database. Rolls back and re-applies migrations.
	"""
	if click.confirm('Do you want to reset your projects database?'):
		click.secho('Resetting your project database...', fg='red')
		reset_db()

flint.add_command(project)
flint.add_command(backer)
flint.add_command(back)
flint.add_command(list)
flint.add_command(reset)
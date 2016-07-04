import click
from utils.db_helpers import *

@click.argument('name')
@click.command()
def backer(name):
	"""
	Lists projects backed by given backer \n
	e.g. backer Starlord
	"""
	rows = BaseDBHandler.pledges_by_backer(name)
	if rows:
		for row in rows:
			click.echo("-- Backed {project} for ${amount:.2f}}".format(project=row['project'], amount=row['amount']))
	else:
		click.echo("{} hasn't backed any projects.".format(name))

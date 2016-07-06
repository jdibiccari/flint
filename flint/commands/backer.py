import click
from utils import *

@click.argument('name')
@click.command()
@pass_dbhandler
def backer(dbhandler, name):
	"""
	Lists projects backed by given backer \n
	e.g. backer Starlord
	"""
	rows = dbhandler.pledges_by_backer(name)
	if rows:
		for row in rows:
			click.echo(get_message(BACKER, 'pledge', {'project': row['project'], 'amount': row['amount']}))
	else:
		click.echo(get_message(BACKER, 'not_found', {'backer': name}))

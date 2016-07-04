import click
from utils.db_handler import *
from utils.notification import *

@click.argument('project')
@click.command()
@pass_dbhandler
def list(dbhandler, project):
	"""
	Displays backers and backed amounts \n
	e.g. list Awesome_Sauce
	"""
	rows = dbhandler.backers_by_project(project)
	if rows:
		to_goal = rows[0]['target_amount'] - rows[0]['amount_raised']
		if rows[0]['backer'] != '':
			for row in rows:
				click.echo(get_message(LIST, 'pledge', {'backer': row['backer'], 'amount': row['amount']}))

		if to_goal <= 0:
			click.echo(get_message(LIST, 'target_reached', {'project': project}))
		else:
			click.echo(get_message(LIST, 'target_not_reached', {'project': project, 'to_goal': to_goal}))
	else:
		click.echo(get_message(LIST, 'not_found', {'project': project}))


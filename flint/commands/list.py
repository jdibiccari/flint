import click
from utils.db_helpers import *

@click.argument('project')
@click.command()
def list(project):
	"""
	Displays backers and backed amounts \n
	e.g. list Awesome_Sauce
	"""
	rows = BaseDBHandler.backers_by_project(project)
	if rows:
		to_goal = rows[0]['target_amount'] - rows[0]['amount_raised']
		if rows[0]['backer'] != '':
			for row in rows:
				click.echo("-- {backer} backed for ${amount:.2f}".format(backer=row['backer'], amount=row['amount']))

		if to_goal <= 0:
			click.echo("{project} is successful!".format(project=project))
		else:
			click.echo("{project} needs ${to_goal:.2f} more to be successful!".format(project=project, to_goal=to_goal))
	else:
		click.echo("There's no project by the name {project}.".format(project=project))


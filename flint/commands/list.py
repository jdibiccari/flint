import click
from utils.db_helpers import db_connect


@click.argument('project')
@click.command()
def list(project):
	"""
	Displays backers and backed amounts \n
	e.g. list Awesome_Sauce
	"""
	conn = db_connect()
	cur = conn.cursor()
	select_sql = """SELECT projects.name as project,
							ifnull(backers.name, '') as backer,
							pledges.amount,
							projects.target_amount,
							projects.amount_raised
						FROM projects
						LEFT JOIN pledges
						ON pledges.project_id=projects.id
						LEFT JOIN backers
						ON pledges.backer_id=backers.id
						WHERE projects.name ='{project}'""".format(project=project)
	cur.execute(select_sql)
	rows = cur.fetchall()
	if rows:
		to_goal = rows[0]['target_amount'] - rows[0]['amount_raised']
		if rows[0]['backer'] != '':
			for row in rows:
				click.echo("-- {backer} backed for ${amount}".format(backer=row['backer'], amount=row['amount']))

		if to_goal <= 0:
			click.echo("{project} is successful!".format(project=rows[0]['project']))
		else:
			click.echo("{project} needs ${to_goal} more to be successful!".format(project=rows[0]['project'], to_goal=to_goal))
	else:
		click.echo("There's no project by the name {project}.".format(project=project))


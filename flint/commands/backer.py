import click
from utils.db_helpers import db_connect


@click.argument('name')
@click.command()
def backer(name):
	"""
	Lists projects backed by given backer \n
	e.g. backer Starlord
	"""
	conn = db_connect()
	cur = conn.cursor()
	select_sql = """SELECT projects.name as project, pledges.amount
					FROM projects
					LEFT JOIN pledges
					ON pledges.project_id=projects.id
					LEFT JOIN backers
					ON pledges.backer_id=backers.id
					WHERE backers.name='{backer}'""".format(backer=name)
	cur.execute(select_sql)
	rows = cur.fetchall()
	if rows:
		for row in rows:
			click.echo("-- Backed {project} for ${amount}".format(project=row['project'], amount=row['amount']))
	else:
		click.echo("{} hasn't backed any projects.".format(name))

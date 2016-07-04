import click
import os
import sqlite3
from yoyo import read_migrations, get_backend
from config_parser import parse

class DBHandler(object):
	def __init__(self, test=False):
		self.migration_directory = parse('database', 'migrations')
		self.db_path = parse('database', 'db_path')
		self.db = parse('database', 'db')
		if test:
			self.test_mode()

	def test_mode(self):
		self.db_path = parse('database', 'test_db_path')
		self.db = parse('database', 'test_db')

	def db_exists(self):
		return os.path.isfile(self.db_path)

	def get_db_migrations(self):
		backend = get_backend(self.db)
		migrations = read_migrations(self.migration_directory)
		return backend, migrations

	def setup_db(self):
		backend, migrations = self.get_db_migrations()
		backend.apply_migrations(backend.to_apply(migrations))

	def reset_db(self):
		backend, migrations = self.get_db_migrations()
		backend.rollback_migrations(backend.to_rollback(migrations))
		backend.apply_migrations(backend.to_apply(migrations))

	def drop_db(self):
		os.remove(self.db_path)

	def connect_to_db(self):
		# Returns a db connection and a cursor for executing queries
		conn = False
		cursor = False
		try:
		    conn=sqlite3.connect(self.db_path)
		    conn.row_factory = sqlite3.Row
		    cursor = conn.cursor()
		except:
			pass
		return conn, cursor

	def find_by(self, table, filters):
		conn, cursor = self.connect_to_db()
		select_criteria = ["{}='{}'".format(k,v) for k, v in filters.iteritems()]
		sql = """SELECT * FROM {table} WHERE {select_criteria}""".format(table=table, select_criteria='AND '.join(select_criteria))
		cursor.execute(sql)
		row = cursor.fetchone()
		conn.close()
		return row

	def create(self, table, filters):
		conn, cursor = self.connect_to_db()
		cols = ', '.join(filters.keys())
		vals = ', '.join(["'{}'".format(val) for val in filters.values()])
		insert_sql = """INSERT INTO {table} ({columns}) VALUES ({values})""".format(table=table, columns=cols, values=vals)
		cursor.execute(insert_sql)
		conn.commit()
		row = self.find_by(table, {'id': cursor.lastrowid})
		conn.close()
		return row

	def find_or_create(self, table, filters):
		row = self.find_by(table, filters)
		if not row:
			row = self.create(table, filters)
		return row

	def update_amount_raised(self, project, amount):
		conn, cursor = self.connect_to_db()
		update_sql = """UPDATE projects
						SET amount_raised = amount_raised + {amount}
						WHERE id={project}""".format(amount=amount, project=project)
		cursor.execute(update_sql)
		conn.commit()
		conn.close()

	def backers_by_project(self, project):
		conn, cursor = self.connect_to_db()
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
		cursor.execute(select_sql)
		return cursor.fetchall()

	def pledges_by_backer(self, backer):
		conn, cursor = self.connect_to_db()
		select_sql = """SELECT projects.name as project, pledges.amount
						FROM projects
						LEFT JOIN pledges
						ON pledges.project_id=projects.id
						LEFT JOIN backers
						ON pledges.backer_id=backers.id
						WHERE backers.name='{backer}'""".format(backer=backer)
		cursor.execute(select_sql)
		return cursor.fetchall()


# A command decorator that allows you to pass your dbhandler to nested commands
pass_dbhandler = click.make_pass_decorator(DBHandler, ensure=True)


import os
import sqlite3
from yoyo import read_migrations, get_backend
from config_parser import parse

class BaseDBHandler(object):
	db_path = parse('database', 'db_path')
	db = parse('database', 'db')
	migration_directory = parse('database', 'migrations')

	@classmethod
	def db_exists(cls):
		return os.path.isfile(cls.db_path)

	@classmethod
	def get_db_migrations(cls):
		backend = get_backend(cls.db)
		migrations = read_migrations(cls.migration_directory)
		return backend, migrations

	@classmethod
	def setup_db(cls):
		backend, migrations = cls.get_db_migrations()
		backend.apply_migrations(backend.to_apply(migrations))

	@classmethod
	def reset_db(cls):
		backend, migrations = cls.get_db_migrations()
		backend.rollback_migrations(backend.to_rollback(migrations))
		backend.apply_migrations(backend.to_apply(migrations))

	@classmethod
	def drop_db(cls):
		os.remove(cls.db_path)

	@classmethod
	def connect_to_db(cls):
		# Returns a db connection and a cursor for executing queries
		conn = False
		cursor = False
		try:
		    conn=sqlite3.connect(cls.db_path)
		    conn.row_factory = sqlite3.Row
		    cursor = conn.cursor()
		except:
			pass
		return conn, cursor

	@classmethod
	def find_by(cls, table, filters):
		conn, cursor = cls.connect_to_db()
		select_criteria = ["{}='{}'".format(k,v) for k, v in filters.iteritems()]
		sql = """SELECT * FROM {table} WHERE {select_criteria}""".format(table=table, select_criteria='AND '.join(select_criteria))
		cursor.execute(sql)
		row = cursor.fetchone()
		conn.close()
		return row

	@classmethod
	def create(cls, table, filters):
		conn, cursor = cls.connect_to_db()
		cols = ', '.join(filters.keys())
		vals = ', '.join(["'{}'".format(val) for val in filters.values()])
		insert_sql = """INSERT INTO {table} ({columns}) VALUES ({values})""".format(table=table, columns=cols, values=vals)
		cursor.execute(insert_sql)
		conn.commit()
		row = cls.find_by(table, {'id': cursor.lastrowid})
		conn.close()
		return row

	@classmethod
	def find_or_create(cls, table, filters):
		row = cls.find_by(table, filters)
		if not row:
			row = cls.create(table, filters)
		return row

	@classmethod
	def update_amount_raised(cls, project, amount):
		conn, cursor = cls.connect_to_db()
		update_sql = """UPDATE projects
						SET amount_raised = amount_raised + {amount}
						WHERE id={project}""".format(amount=amount, project=project)
		cursor.execute(update_sql)
		conn.commit()
		conn.close()

	@classmethod
	def backers_by_project(cls, project):
		conn, cursor = cls.connect_to_db()
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

	@classmethod
	def pledges_by_backer(cls, backer):
		conn, cursor = cls.connect_to_db()
		select_sql = """SELECT projects.name as project, pledges.amount
						FROM projects
						LEFT JOIN pledges
						ON pledges.project_id=projects.id
						LEFT JOIN backers
						ON pledges.backer_id=backers.id
						WHERE backers.name='{backer}'""".format(backer=backer)
		cursor.execute(select_sql)
		return cursor.fetchall()

class TestDBHandler(BaseDBHandler):
	db_path = parse('database', 'test_db_path')
	db = parse('database', 'test_db')



# def get_message(outcome, replace_with):
# 	OUTCOMES = {
# 		'no_project': 'There\'s no project by the name {project}.',
# 		'target_reached': '{project} is successful!',
# 		'target_not_reached': '{project} needs ${to_goal:.2f} more to be successful!',
# 	}
# 	return OUTCOMES['outcome'].format(**replace_with)


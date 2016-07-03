import os
import sqlite3
from yoyo import read_migrations, get_backend
from config_parser import parse
# Haven't decided if I'm going down the OO route yet
# from abc import ABCMeta, abstractproperty
# class Model(object):
# 	table = None
# 	__metaclass__ = ABCMeta

# 	@abstractproperty
# 	def __repr__(self):
# 		""""Return a string representation of the instance"""
# 		pass

# 	@classmethod
# 	def __table__(cls):
# 		return cls.__name__.lower()

# 	@classmethod
# 	def connect_to_db(cls):
# 		conn = False
# 		try:
# 		    conn=sqlite3.connect('../../db/flint.sqlite')
# 		    conn.row_factory = sqlite3.Row
# 		except:
# 			pass
# 		return conn

# 	@classmethod
# 	def find_by(cls, filters):
# 		conn = cls.connect_to_db()
# 		cursor = conn.cursor()
# 		select_criteria = ["{}='{}'".format(k,v) for k, v in filters.iteritems()]
# 		sql = """SELECT * FROM {table} WHERE {select_criteria}""".format(table=cls.__table__(), select_criteria='AND '.join(select_criteria))
# 		# Add some error handling around these
# 		cursor.execute(sql)
# 		row = cursor.fetchone()
# 		conn.close()
# 		return row

# 	@classmethod
# 	def create(cls, filters):
# 		conn = cls.connect_to_db()
# 		cursor = conn.cursor()
# 		cols = ', '.join(filters.keys())
# 		vals = ', '.join(["'{}'".format(val) for val in filters.values()])
# 		insert_sql = """INSERT INTO {table} ({columns}) VALUES ({values})""".format(table=cls.__table__(), columns=cols, values=vals)
# 		cursor.execute(insert_sql)
# 		conn.commit()
# 		row = cls.find_by({'id': cursor.lastrowid})
# 		conn.close()
# 		return row

# 	@classmethod
# 	def find_or_create(cls, filters):
# 		row = cls.find_by(table, filters)
# 		if not row:
# 			row = cls.create(table, filters)
# 		return row

# class Projects(Model):
# 	def __init__(self, name, target_amount):
# 		self.name = name
# 		self.target_amount = target_amount

# 	def __repr__(self):
# 		return '{name} | {target}'.format(name=self.name, target=self.target_amount)

# 	@classmethod
# 	def update_amount_raised(cls, project, amount):
# 		conn = cls.connect_to_db()
# 		cursor = conn.cursor()
# 		update_sql = """UPDATE {table}
# 						SET amount_raised = amount_raised + {amount}
# 						WHERE id={project}""".format(table=cls.__table__(), amount=amount, project=project)
# 		cursor.execute(update_sql)
# 		conn.commit()
# 		conn.close()

db_path = parse('database', 'db_path')
db = parse('database', 'db')
migration_directory = parse('database', 'migrations')

def db_exists():
	return os.path.isfile(db_path)

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

#create db connection
def connect_to_db():
	# Returns a db connection and a cursor for executing queries
	conn = False
	cursor = False
	try:
	    conn=sqlite3.connect(db_path)
	    conn.row_factory = sqlite3.Row
	    cursor = conn.cursor()
	except:
		pass
	return conn, cursor

def find_by(table, filters):
	conn, cursor = connect_to_db()
	select_criteria = ["{}='{}'".format(k,v) for k, v in filters.iteritems()]
	sql = """SELECT * FROM {table} WHERE {select_criteria}""".format(table=table, select_criteria='AND '.join(select_criteria))
	cursor.execute(sql)
	row = cursor.fetchone()
	conn.close()
	return row

def create(table, filters):
	conn, cursor = connect_to_db()
	cols = ', '.join(filters.keys())
	vals = ', '.join(["'{}'".format(val) for val in filters.values()])
	insert_sql = """INSERT INTO {table} ({columns}) VALUES ({values})""".format(table=table, columns=cols, values=vals)
	cursor.execute(insert_sql)
	conn.commit()
	row = find_by(table, {'id': cursor.lastrowid})
	conn.close()
	return row

def find_or_create(table, filters):
	row = find_by(table, filters)
	if not row:
		row = create(table, filters)
	return row


def update_amount_raised(project, amount):
	conn, cursor = connect_to_db()
	update_sql = """UPDATE projects
					SET amount_raised = amount_raised + {amount}
					WHERE id={project}""".format(amount=amount, project=project)
	cursor.execute(update_sql)
	conn.commit()
	conn.close()

def backers_by_project(project):
	conn, cursor = connect_to_db()
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

def pledges_by_backer(backer):
	conn, cursor = connect_to_db()
	select_sql = """SELECT projects.name as project, pledges.amount
					FROM projects
					LEFT JOIN pledges
					ON pledges.project_id=projects.id
					LEFT JOIN backers
					ON pledges.backer_id=backers.id
					WHERE backers.name='{backer}'""".format(backer=backer)
	cursor.execute(select_sql)
	return cursor.fetchall()

# def get_message(outcome, replace_with):
# 	OUTCOMES = {
# 		'no_project': 'There\'s no project by the name {project}.',
# 		'target_reached': '{project} is successful!',
# 		'target_not_reached': '{project} needs ${to_goal:.2f} more to be successful!',
# 	}
# 	return OUTCOMES['outcome'].format(**replace_with)


import sqlite3
from abc import ABCMeta, abstractproperty

# Haven't decided if I'm going down the OO route yet
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
# 	def db_connect(cls):
# 		conn = False
# 		try:
# 		    conn=sqlite3.connect('../../db/flint.sqlite')
# 		    conn.row_factory = sqlite3.Row
# 		except:
# 			pass
# 		return conn

# 	@classmethod
# 	def find_by(cls, filters):
# 		conn = cls.db_connect()
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
# 		conn = cls.db_connect()
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
# 		conn = cls.db_connect()
# 		cursor = conn.cursor()
# 		update_sql = """UPDATE {table}
# 						SET amount_raised = amount_raised + {amount}
# 						WHERE id={project}""".format(table=cls.__table__(), amount=amount, project=project)
# 		cursor.execute(update_sql)
# 		conn.commit()
# 		conn.close()


def find_by(table, filters):
	conn = db_connect()
	cursor = conn.cursor()
	select_criteria = ["{}='{}'".format(k,v) for k, v in filters.iteritems()]
	sql = """SELECT * FROM {table} WHERE {select_criteria}""".format(table=table, select_criteria='AND '.join(select_criteria))
	cursor.execute(sql)
	row = cursor.fetchone()
	conn.close()
	return row

def update_amount_raised(project, amount):
	conn = db_connect()
	cursor = conn.cursor()
	update_sql = """UPDATE projects
					SET amount_raised = amount_raised + {amount}
					WHERE id={project}""".format(amount=amount, project=project)
	cursor.execute(update_sql)
	conn.commit()
	conn.close()

def create(table, filters):
	conn = db_connect()
	cursor = conn.cursor()
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

#create db connection
def db_connect():
	conn = False
	try:
	    conn=sqlite3.connect('db/flint.sqlite')
	    conn.row_factory = sqlite3.Row
	except:
		pass
	return conn
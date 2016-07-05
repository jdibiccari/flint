"""
Create projects table
"""

from yoyo import step

__depends__ = {'__init__'}

step(
    """CREATE TABLE projects
	    (id INTEGER PRIMARY KEY,
	    name VARCHAR(20) NOT NULL UNIQUE,
	    target_amount INT NOT NULL,
	    amount_raised INT DEFAULT 0)""",
    "DROP TABLE projects",
)


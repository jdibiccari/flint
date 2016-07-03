"""
Create backers table
"""

from yoyo import step

__depends__ = {'flint_20160629_01_0FFYh'}

step(
    "CREATE TABLE backers (id INTEGER PRIMARY KEY, name VARCHAR(20) NOT NULL UNIQUE)",
    "DROP TABLE backers",
)
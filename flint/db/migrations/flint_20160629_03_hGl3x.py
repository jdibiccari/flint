"""
Create pledges table
"""

from yoyo import step

__depends__ = {'flint_20160629_02_oz2al'}

step(
    """CREATE TABLE pledges (id INTEGER PRIMARY KEY, backer_id INTEGER, project_id INTEGER, amount INTEGER,
    UNIQUE(backer_id, project_id),
    FOREIGN KEY(backer_id) REFERENCES backer(id),
    FOREIGN KEY(project_id) REFERENCES project(id))""",
    """DROP TABLE pledges""",
)

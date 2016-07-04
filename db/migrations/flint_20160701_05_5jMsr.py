"""
Create backer_cards table
"""

from yoyo import step

__depends__ = {'flint_20160701_04_bl5TA'}

step(
    """CREATE TABLE backer_cards (id INTEGER PRIMARY KEY, backer_id INTEGER NOT NULL, credit_card_id INTEGER NOT NULL UNIQUE)""",
    """DROP TABLE backer_cards""",
)
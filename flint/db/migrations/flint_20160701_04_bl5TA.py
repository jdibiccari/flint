"""
Create credit card table
"""

from yoyo import step

__depends__ = {'flint_20160629_03_hGl3x'}

step(
    """CREATE TABLE credit_cards (id INTEGER PRIMARY KEY, card_number VARCHAR(19) NOT NULL UNIQUE)""",
    """DROP TABLE credit_cards""",
)
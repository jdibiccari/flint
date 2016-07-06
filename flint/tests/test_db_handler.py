import unittest
from flint.commands.utils import *

class TestDBHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dbhandler = DBHandler(test=True)
        dbhandler.reset_db()

    def test_connect_to_db(self):
        """It returns a sqlite3 db connection"""
        dbhandler = DBHandler(test=True)
        conn, _ = dbhandler.connect_to_db()
        self.assertIsInstance(conn, sqlite3.Connection)

    def test_create(self):
        """It creates a row from provided values """
        dbhandler = DBHandler(test=True)
        result = dbhandler.create('projects', {'name': 'MoonLanding', 'target_amount': 200000})
        self.assertIsInstance(result, sqlite3.Row)

    def test_find_by(self):
        """It returns the appropriate sqlite3 row"""
        dbhandler = DBHandler(test=True)
        dbhandler.create('projects', {'name': 'Awesome_Sauce', 'target_amount': 900})
        result = dbhandler.find_by('projects', {'name': 'Awesome_Sauce'})
        self.assertEqual(result['name'], 'Awesome_Sauce')

    def test_find_by_no_result(self):
        """It returns None if the row doesn't exist"""
        dbhandler = DBHandler(test=True)
        result = dbhandler.find_by('projects', {'name': 'Awesome-Sauce'})
        self.assertIsNone(result)

    def test_update_amt_raised(self):
        """It updates a projects amount_raised"""
        dbhandler = DBHandler(test=True)
        project = dbhandler.create('projects', {'name': 'Started-From-the-Bottom', 'target_amount': 900})
        dbhandler.update_amount_raised(project['id'], '20')
        result = dbhandler.find_by('projects', {'name': 'Started-From-the-Bottom'})
        self.assertEqual(result['amount_raised'], 20)

    @classmethod
    def tearDownClass(cls):
        dbhandler = DBHandler(test=True)
        dbhandler.drop_db()

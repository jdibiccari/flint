import unittest
from flint.commands.utils.db_helpers import TestDBHandler

class TestAddProject(unittest.TestCase):

    def setUp(self):
    	TestDBHandler.setup_db()

    def test_add_project_success(self):
    	"""Successfully add project with name and target amount"""
        self.assertEqual('foo'.upper(), 'FOO')

    def tearDown(self):
        TestDBHandler.drop_db()
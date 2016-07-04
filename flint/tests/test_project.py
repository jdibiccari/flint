import unittest
from subprocess import PIPE, Popen as popen
from flint.commands.utils.db_helpers import TestDBHandler

class TestAddProject(unittest.TestCase):

    def setUp(self):
    	TestDBHandler.setup_db()

    def test_add_project_success(self):
    	"""Successfully add project with name and target amount"""
    	output = popen(['flint', 'project', 'Awesome_Sauce', 900], stdout=PIPE).communicate()[0]
    	self.assertEqual(output, 'Added Awesome_Sauce_o project with target of $900.00')

    def tearDown(self):
        TestDBHandler.drop_db()
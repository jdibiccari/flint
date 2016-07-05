import unittest
from click.testing import CliRunner
from flint.commands.utils import *
from flint.cli import flint

class TestProjectInterface(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        dbhandler = DBHandler(test=True)
        dbhandler.reset_db()

    def test_error_duplicate(self):
        """It shows an error msg when you add a project with the same name"""
        runner = CliRunner()
        for _ in xrange(2):
            result = runner.invoke(flint, ['-t', 'project', 'Galaxy_Guardian', '200'])
        expected_output = get_message(PROJECT, 'project_nonunique')
        self.assertEqual(result.output.strip('\n'), expected_output)

    def test_error_name(self):
        """It shows an error msg when you add a project with an invalid name"""
        runner = CliRunner()
        result = runner.invoke(flint, ['-t', 'project', '###Unicorns!!###', '200'])
        expected_output = get_message(VALIDATION, 'invalid_name', {'name': '###Unicorns!!###'})
        self.assertEqual(result.output.strip('\n'), expected_output)

    def test_success(self):
        """It shows a success msg when you add a project with a valid name and target amount"""
        runner = CliRunner()
        result = runner.invoke(flint, ['-t', 'project', 'Awesome_Sauce', '900'])
        expected_output = get_message(PROJECT, 'success', {'project': 'Awesome_Sauce', 'target': 900})
        self.assertEqual(result.output.strip('\n'), expected_output)

    @classmethod
    def tearDownClass(cls):
        dbhandler = DBHandler(test=True)
        dbhandler.drop_db()
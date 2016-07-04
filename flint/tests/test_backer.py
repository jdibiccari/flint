import unittest
from click.testing import CliRunner
from flint.commands.utils import *
from flint.cli import flint

class TestBackerInterface(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        dbhandler = DBHandler(test=True)
        dbhandler.reset_db()

    def test_backer_list_pledge(self):
        """It lists all pledges the backer has made"""

        # Setup some projects and back them
        projects = [
            {'project': 'Galaxy_Guardian', 'amount': 200},
            {'project': 'MysteriousOrb', 'amount': 1000}
        ]
        runner = CliRunner()
        expected_output = []
        for project in projects:
            runner.invoke(flint, ['-t', 'project', project['project'], str(project['amount'])])
            runner.invoke(flint, ['-t', 'back', 'Star-Lord', project['project'], '4532175168706355', str(project['amount'])])
            expected_output.append(
                get_message(BACKER, 'pledge', project)
            )

        result = runner.invoke(flint, ['-t', 'backer', 'Star-Lord'])
        self.assertEqual(result.output.strip('\n'), '\n'.join(expected_output))

    def test_backer_not_found(self):
        """It informs if the backer doesn't exist"""
        runner = CliRunner()
        result = runner.invoke(flint, ['-t', 'backer', 'Nebula'])
        expected_output = get_message(BACKER, 'not_found', {'backer': 'Nebula'})
        self.assertEqual(result.output.strip('\n'), expected_output)

    @classmethod
    def tearDownClass(cls):
        dbhandler = DBHandler(test=True)
        dbhandler.drop_db()
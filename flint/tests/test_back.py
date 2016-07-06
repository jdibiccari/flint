import unittest
from click.testing import CliRunner
from flint.commands.utils import *
from flint.cli import flint

class TestBackInterface(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        dbhandler = DBHandler(test=True)
        dbhandler.reset_db()

    def test_back_success(self):
        """It lists the details of a successful backing"""
        pledge = {'backer': 'Dave', 'project': 'Awesome_Sauce', 'amount': 90}
        runner = CliRunner()
        runner.invoke(flint, ['-t', 'project', pledge['project'], '900'])
        result = runner.invoke(flint, ['-t', 'back', pledge['backer'], pledge['project'], '4532175168706355', str(pledge['amount'])])

        expected_output = get_message(BACK, 'success', pledge)
        self.assertEqual(result.output.strip('\n'), expected_output)

    def test_back_project_not_found(self):
        """It informs if the project doesn't exist"""
        runner = CliRunner()
        result = runner.invoke(flint, ['-t', 'back', 'Janel', 'Not-a-Project', '6011905380521199', '90'])
        expected_output = get_message(BACK, 'project_not_found')
        self.assertEqual(result.output.strip('\n'), expected_output)

    def test_back_backer_nonunique(self):
        """It informs if the backer has already backed the project"""
        runner = CliRunner()
        runner.invoke(flint, ['-t', 'project', 'HavingItAll', '100'])
        for _ in xrange(2):
            result = runner.invoke(flint, ['-t', 'back', 'Janel', 'HavingItAll', '4532725532898187', '90'])
        expected_output = get_message(BACK, 'backer_nonunique')
        self.assertEqual(result.output.strip('\n'), expected_output)

    def test_back_card_nonunique(self):
        """It informs if the card has been added by another user"""
        runner = CliRunner()
        runner.invoke(flint, ['-t', 'project', 'Jenna_and_Paul', '100'])
        runner.invoke(flint, ['-t', 'back', 'Lauren', 'Jenna_and_Paul', '6011420832844967', '50'])
        result = runner.invoke(flint, ['-t', 'back', 'Janel', 'Jenna_and_Paul', '6011420832844967', '50'])
        expected_output = get_message(BACK, 'card_nonunique')
        self.assertEqual(result.output.strip('\n'), expected_output)

    @classmethod
    def tearDownClass(cls):
        dbhandler = DBHandler(test=True)
        dbhandler.drop_db()
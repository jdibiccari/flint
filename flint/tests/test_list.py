import unittest
from click.testing import CliRunner
from flint.commands.utils import *
from flint.cli import flint

class TestListInterface(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        dbhandler = DBHandler(test=True)
        dbhandler.reset_db()

    def test_list_project_not_found(self):
        """It shows an error msg when it can't find the project"""
        runner = CliRunner()
        result = runner.invoke(flint, ['-t', 'list', 'A_Project_Has_No_Name'])
        expected_output = get_message(LIST, 'not_found', {'project': 'A_Project_Has_No_Name'})
        self.assertEqual(result.output.strip('\n'), expected_output)

    def test_list_project_pledges_target(self):
        """It lists all pledges and informs that project target not reached"""
        runner = CliRunner()
        # Setup project with pledges
        runner.invoke(flint, ['-t', 'project', '30_Rock_Returns', '300'])
        pledges = [
            {'amount': 100, 'backer': 'Liz_Lemon', 'card': 348501267643300},
            {'amount': 100, 'backer': 'Jenna_Maroney', 'card': 348501267643300}
        ]
        expected_output = []
        for pledge in pledges:
            runner.invoke(flint, ['-t', 'back', pledge['backer'], '30_Rock_Returns', pledge['card'], str(project['amount'])])
            expected_output.append(
                get_message(LIST, 'pledge', pledge)
            )
        expected_output.append(get_message([LIST], 'target_not_reached', {'project': '30_Rock_Returns', 'target_amount': 300}))
        self.assertEqual(result.output.strip('\n'), expected_output)

    def test_list_project_pledges_target(self):
        """It lists all pledges and informs that project target reached"""
        pass

    @classmethod
    def tearDownClass(cls):
        dbhandler = DBHandler(test=True)
        dbhandler.drop_db()
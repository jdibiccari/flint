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

    def test_list_project_pledges_target_not_reached(self):
        """It lists all pledges and informs that project target not reached"""
        expected_output = []
        project = '30_Rock_Returns'
        pledges = [
            {'amount': 100, 'backer': 'Liz_Lemon', 'card': 348501267643300},
            {'amount': 100, 'backer': 'Jenna_Maroney', 'card': 377242569628624}
        ]
        runner = CliRunner()
        runner.invoke(flint, ['-t', 'project', project, '300'])

        for pledge in pledges:
            runner.invoke(
                flint, ['-t', 'back', pledge['backer'], project, str(pledge['card']), str(pledge['amount'])]
            )
            expected_output.append(
                get_message(LIST, 'pledge', pledge)
            )

        expected_output.append(
            get_message(LIST, 'target_not_reached', {'project': project, 'to_goal': 100})
        )
        result = runner.invoke(flint, ['-t', 'list', project])
        self.assertEqual(result.output.strip('\n'), '\n'.join(expected_output))

    def test_list_project_pledges_target_reached(self):
        """It lists all pledges and informs that project target reached"""
        project = 'Popcorn_Organizer'
        pledge = {'amount': 10, 'backer': 'Kenneth', 'card': 5407598252092029}

        runner = CliRunner()
        runner.invoke(flint, ['-t', 'project', project, '10'])
        runner.invoke(flint, ['-t', 'back', pledge['backer'], project, str(pledge['card']), str(pledge['amount'])])
        result = runner.invoke(flint, ['-t', 'list', project])
        expected_output = get_message(LIST, 'pledge', pledge) + '\n' + get_message(LIST, 'target_reached', {'project': project})
        self.assertEqual(result.output.strip('\n'), expected_output)

    @classmethod
    def tearDownClass(cls):
        dbhandler = DBHandler(test=True)
        dbhandler.drop_db()
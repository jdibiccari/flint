import unittest
import flint

class TestAddProject(unittest.TestCase):

    def setUp(self):
    	pass

    def test_add_project_success(self):
    	"""Successfully add project with name and target amount"""
        self.assertEqual('foo'.upper(), 'FOO')

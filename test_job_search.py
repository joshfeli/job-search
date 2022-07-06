import unittest
import job_search
from mock_job_results import mock_results
import pdb

class TestJobSearch(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_enter_into_database(self):
        # will have to update to make a fake database for tests
        engine = job_search.enter_into_database(mock_results)
        query_result = engine.execute('SELECT * FROM jobs;').fetchall()
        self.assertIs(type(query_result), dict)
        self.assertEqual(len(query_result), 3)
        
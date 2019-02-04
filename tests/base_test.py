from app import polApp
from instance.config import configs
import unittest
import json

class BaseTest(unittest.TestCase):
    '''Sets up the initial repeated tasks for all tests'''

    def setUp(self):
        polApp.config.from_object(configs['testing'])
        self.client = polApp.test_client

        


    def test_home(self):
        result = self.client().get('/')
        dataCheck = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue('status' in dataCheck)
        self.assertEqual(dataCheck['status'], 200)
        



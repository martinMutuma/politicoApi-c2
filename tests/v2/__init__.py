import random
import string
from instance.config import configs
import unittest
import json
from app import create_app
from app.db_setup import DbSetup
from run import polApp

config = "testing"

db = DbSetup(config)


class BaseTest(unittest.TestCase):
    '''Sets up the initial repeated tasks for all tests'''

    def setUp(self):
        db.create_tables()
        polApp.config.from_object(configs['testing'])
        self.client = polApp.test_client

    def post(self, path, data={}):
        result = self.client().post(path=path, data=data)
        return result

    def check_standard_reply(self, datacheck, status, error=False):
        self.assertTrue('status' in datacheck)
        if not error:
            self.assertTrue('data' in datacheck)
        else:
            self.assertTrue('error' in datacheck)

    @staticmethod
    def random_name(stringLength=10):
        """Generate a random string with the combination of lowercase and uppercase letters """
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(stringLength))

    def tearDown(self):
        pass
        # db.drop()

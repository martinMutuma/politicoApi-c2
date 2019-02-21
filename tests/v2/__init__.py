import random
import string
from instance.config import configs
import unittest
import json
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
        result = self.send_auth_request(path, 'POST', data)
        return result

    def check_standard_reply(self, datacheck, status, error=False):
        self.assertTrue('status' in datacheck)
        if not error:
            self.assertTrue('data' in datacheck)
        else:
            self.assertTrue('error' in datacheck)

    @staticmethod
    def random_name(stringLength=10):
        """Generate a random string with
        the combination of lowercase and uppercase letters
         """
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(stringLength))

    def send_auth_request(self, Url, method, data={}):
        """Fore adding headers to request
        """
        return self.client().open(Url,
                                  method=method,
                                  headers={
                                      'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MywiZW1haWwiOiJhZG1pbkBtYWlsLmNvbSIsImZpcnN0bmFtZSI6Ik5hbWUiLCJvdGhlcm5hbWUiOiJPdGhlck5hbWUiLCJsYXN0bmFtZSI6IldlbGxuYW1lIiwicGhvbmVudW1iZXIiOiIwODkzMjkyOTkyIiwicGFzc3BvcnR1cmxzdHJpbmciOiJ3d3cudXJsLmNvbS8xNiIsImlzYWRtaW4iOnRydWV9.Xow6qYFh8yrqQ-gwMEp4DLtpYZVW-KA2oRtugQr79XA",  "Content-Type": "application/json"
                                  },
                                  data=json.dumps(data)
                                  )

    def generate_random_office(self):
        return {
            'name': BaseTest().random_name(10),
            'type': 'state'
        }

    def generate_user(self):
        return {
            "email": "email{}@mail.com".format(BaseTest.random_name(6)),
            "password": "password",
            "firstname": "Name",
            "othername": "OtherName",
            "lastname": "Wellname",
            "phonenumber": "089329296692",
            "passporturlstring": "www.url.com/"+BaseTest.random_name(9)
        }

    def gen_party(self):
        return {
            'name': BaseTest().random_name(10),
            'hqAddress': '23 jumpstreet',
            'logoUrl': 'www.url.com/ ' + BaseTest().random_name(10),
        }

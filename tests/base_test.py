
from instance.config import configs
import unittest
import json
from run import polApp


class BaseTest(unittest.TestCase):
    '''Sets up the initial repeated tasks for all tests'''

    def setUp(self):
        polApp.config.from_object(configs['testing'])
        self.client = polApp.test_client

        
    def post(self , path, data={}):
        result = self.client().post(path=path, data=data)
        return result

    def test_default_route(self):
        result = self.client().get('/')
        print(result.__dict__)
        self.assertEqual(result.status_code, 200)

        dataCheck = json.loads(result.data)
        self.assertTrue('status' in dataCheck)
        

    def test_page_not_found(self):
        result = self.client().get('/page_not_found')
        dataCheck = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.check_standard_reply(dataCheck, 404, error=True)
  
    def test_method_not_allowed(self):
        result = self.client().post('/')
        dataCheck = json.loads(result.data)
        self.assertEqual(result.status_code, 405)
        self.check_standard_reply(dataCheck, 405, error=True)

    def check_standard_reply(self, datacheck, status, error=False):
        self.assertTrue('status' in datacheck)
        if not error:
            self.assertTrue('data' in datacheck)
        else:
            self.assertTrue('error' in datacheck)

    def tearDown(self):
        self.client().get('/api/v1/d')

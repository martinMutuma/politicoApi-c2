"""app/test/test_v1_offices.py """
import json
from instance.config import configs
from tests.base_test import BaseTest
from app import polApp


class TestOffices(BaseTest):
    """ 
    Test endpoints  app/v1/offices 
    """

    def test_create_office(self):
        office = {
        'name': 'Office A',
        'type': 'state'
        }
        
        result = self.client().post("/api/v1/offices", data=office)
        self.assertEqual(result.status_code, 201)
        dataCheck = json.loads(result.data)
        
        self.check_standard_reply(dataCheck, 201)
        self.assertEqual(dataCheck['data']['name'], office['name'])

    def test_get_specific_office_details(self):
        office2 = {
        'name': 'Office B',
        'type': 'legislative'
        }
        result = self.client().post("/api/v1/offices", data=office2)
        dataCheck = json.loads(result.data)

        result_get = self.client().get("/api/v1/offices/{}".format(dataCheck['data']['id']))
        self.assertEqual(result_get.status_code, 200)

        data_check_get = json.loads(result_get)
        self.check_standard_reply(dataCheck, 200 )
        self.assertEqual(data_check_get['data']['name'],office2['name'])
        
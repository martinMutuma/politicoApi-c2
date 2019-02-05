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
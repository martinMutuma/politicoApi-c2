"""app/test/test_v1_offices.py """
import json
from instance.config import configs
from tests.base_test import BaseTest
from app import polApp


class TestOffices(BaseTest):
    """ 
    Test endpoints  app/v1/offices 
    """
    office1 = {
        'name': 'Office A',
        'type': 'state'
        }

    office1d = {
        'name': 'Office b',
        'type': 'state'
        }
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

        data_check_get = json.loads(result_get.data)
        self.check_standard_reply(data_check_get, 200 )
        self.assertEqual(data_check_get['data']['name'],office2['name'])
        

    def test_get_all_offices(self):
        office3 = {
            'name': 'Office c',
            'type': 'legislative'
            }
        self.client().post("/api/v1/offices", data=office3)
        result_get = self.client().get("/api/v1/offices")
        self.assertEqual(result_get.status_code, 200)

        data_check_get = json.loads(result_get.data)
        self.check_standard_reply(data_check_get, 200 )

    def test_update_office_name(self):
        """Tests for Patch Data /api/v1/offices/<int:officeid>/name"""
        result12 = self.post('/api/v1/offices', data=self.office1d)
        dataCheck = json.loads(result12.data)
        patch_data = {'name': 'Change Office Name'}
        result = self.client().patch('/api/v1/offices/{}/name'.format(dataCheck['data']['id']), 
                                        data=patch_data)

        self.assertEqual(result.status_code, 202)

        datacheck = json.loads(result.data)
        self.check_standard_reply(datacheck, 202)
        self.assertEqual(datacheck['data']['name'], patch_data['name'])

    def test_delete_office(self):
        """Tests for [DELETE] /api/v1/offices/<int:officeId>to delete office"""
        result12 = self.post('/api/v1/offices', data=self.office1d)
        dataCheck = json.loads(result12.data)

        result = self.client().delete("/api/v1/offices/{}".format(dataCheck['data']['id']))
        self.assertEqual(result.status_code, 200)
        
        datacheck2 = json.loads(result.data)
        self.check_standard_reply(datacheck2, 200)
        self.assertTrue('message' in datacheck2['data'])
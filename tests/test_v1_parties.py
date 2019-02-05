"""app/test/test_v1_party_create.py """
import json
from instance.config import configs
from tests.base_test import BaseTest
from app import polApp


class TestParties(BaseTest):
    """ Test endpoints  app/v1/parties """
    party1 = {
        'name': 'Party A',
        'hqAddress': '22 jumpstreet',
        'logoUrl': 'www.url.com/party.png',
    }
    party1b = {
        'name': 'Party B',
        'hqAddress': '23 jumpstreet',
        'logoUrl': 'www.url.com/party.png',
    }
    party2 = {
        'name': 'Par',
        'hqAddress': '21 jumpstreet',
        'logoUrl': 'www.url.com/party.png',
    }
    party3 = {
        'name': 'Par',
        'logoUrl': 'www.url.com/party.png',
    }

    def setUp(self):
        polApp.config.from_object(configs['testing'])
        self.client = polApp.test_client
        self.result1 = self.client().post('/api/v1/parties', data=self.party1)


    def test_create_party(self):
        """ api/v1/parties Post test """
        result = self.client().post('/api/v1/parties', data=self.party1)
        dataCheck = json.loads(result.data)
        self.assertEqual(result.status_code, 201)
        self.assertTrue('status' in dataCheck)
        self.assertEqual(dataCheck['status'], 201)
        self. assertTrue('data' in dataCheck)
        self.assertTrue('id' in dataCheck['data'])
        self.assertTrue(isinstance(dataCheck['data']['id'], int))
        self.assertEqual(dataCheck['data']['name'], self.party1['name'])

    def test_create_party_with_wrong_data(self):
        """ api/v1/parties Post test with invalid data"""
        result = self.client().post('/api/v1/parties', data=self.party2)
        dataCheck = json.loads(result.data)
        result2 = self.client().post('/api/v1/parties', data=self.party3)
        dataCheck2 = json.loads(result.data)

        self.assertEqual(result.status_code, 400)
        self.assertTrue('status' in dataCheck)
        self.assertEqual(dataCheck['status'], 400)
        self.assertTrue('error' in dataCheck)

        self.assertEqual(result2.status_code, 400)
        self.assertTrue('status' in dataCheck2)
        self.assertEqual(dataCheck2['status'], 400)
        self.assertTrue('error' in dataCheck2)

    def test_get_specifi_party_details(self):
        """tests for endpoint /api/v1/parties/<partyId>"""
        result12 = self.client().post('/api/v1/parties', data=self.party1b)
        dataCheck = json.loads(result12.data)
        resultGet1 = self.client().get(
            "/api/v1/parties/{}".format(dataCheck['data']['id']))
        self.assertEqual(resultGet1.status_code, 200)

        dataCheckGet = json.loads(resultGet1.data)
        self.check_standard_reply(dataCheckGet, 200)

        self.assertEqual(dataCheckGet['data']['name'], dataCheck['data']['name'])

    def test_get_all_parties(self):
        """Test get parties"""
        resultGet = self.client().get("/api/v1/parties/")
        self.assertEqual(resultGet.status_code, 200)

        dataCheckGet = json.loads(resultGet.data)
        self.check_standard_reply(dataCheckGet, 200)

    def test_update_party_name(self):
        """Tests for Patch Data /api/v1/parties/<int:partyid>/name"""
        patch_data = {'name': 'Change Party Name'}
        result = self.client().patch('/api/v1/parties/1/name', data=patch_data)

        self.assertEqual(result.status_code, 202)

        datacheck = json.loads(result.data)
        self.check_standard_reply(datacheck, 202)
        self.assertEqual(datacheck['data']['name'], patch_data['name'])

    def test_delete_party(self):
        """Tests for [DELETE] /api/v1/parties/<int:partyId>to delete party"""
        dataCheckp = json.loads(self.result1.data)
        result = self.client().delete('/api/v1/parties/{}'.format(dataCheckp['data']['id']))
        datacheck = json.loads(result.data)
        self.check_standard_reply(datacheck, 200)
        self.assertTrue('message' in datacheck['data'])

    def check_standard_reply(self, datacheck, status, error=False):
        self.assertTrue('status' in datacheck)
        if not error:
            self.assertTrue('data' in datacheck)
        else:
            self.assertTrue('error' in datacheck)

        self.assertEqual(datacheck['status'], status)

"""app/test/v2/test_party_create.py """
import json
from tests.v2 import BaseTest


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
    party1c = {
        'name': 'Party c',
        'hqAddress': '23 jumpstreet',
        'logoUrl': 'www.url.com/party.png',
    }
    party1d = {
        'name': 'Party D',
        'hqAddress': '23 jumpstreet',
        'logoUrl': 'www.url.com/party.png',
    }
    party_short_name = {
        'name': 'Par',
        'hqAddress': '21 jumpstreet',
        'logoUrl': 'www.url.com/party.png',
    }
    party_missing_data = {
        'name': 'Par',
        'logoUrl': 'www.url.com/party.png',
    }

    def test_create_party(self):
        """ api/v2/parties Post test """
        party1 = self.gen_party()
        result = self.post('/api/v2/parties', data=party1)
        dataCheck = json.loads(result.data)
        self.assertEqual(result.status_code, 201)
        self.assertTrue('status' in dataCheck)
        self.assertEqual(dataCheck['status'], 201)
        self. assertTrue('data' in dataCheck)
        self.assertTrue('id' in dataCheck['data'])
        self.assertEqual(dataCheck['data']['name'], party1['name'])

    def test_create_party_with_wrong_data(self):
        """ api/v2/parties Post test with invalid data"""
        result = self.post('/api/v2/parties', data=self.party_short_name)
        dataCheck = json.loads(result.data)
        result2 = self.post('/api/v2/parties', data=self.party_missing_data)
        dataCheck2 = json.loads(result.data)

        self.assertEqual(result.status_code, 400)
        self.assertTrue('status' in dataCheck)
        self.assertEqual(dataCheck['status'], 400)
        self.assertTrue('error' in dataCheck)

        self.assertEqual(result2.status_code, 400)
        self.assertTrue('status' in dataCheck2)
        self.assertEqual(dataCheck2['status'], 400)
        self.assertTrue('error' in dataCheck2)

    def test_get_party_details(self):
        """tests for endpoint /api/v2/parties/<partyId>"""
        party1c = self.gen_party()

        result12 = self.post('/api/v2/parties', data=party1c)
        dataCheck = json.loads(result12.data)
        resultGet1 = self.send_auth_request(
            "/api/v2/parties/{}".format(dataCheck['data']['id']), 'GET')
        self.assertEqual(resultGet1.status_code, 200)

        dataCheckGet = json.loads(resultGet1.data)
        self.check_standard_reply(dataCheckGet, 200)

        self.assertEqual(dataCheckGet['data']
                         ['name'], dataCheck['data']['name'])

    def test_get_party_details_party_not_exist(self):
        resultGet1 = self.send_auth_request(
            "/api/v2/parties/7676676898", 'GET')
        self.assertEqual(resultGet1.status_code, 404)

        dataCheckGet = json.loads(resultGet1.data)
        self.check_standard_reply(dataCheckGet, 404, True)

    def test_get_all_parties(self):
        """Test get parties"""
        resultGet = self.send_auth_request("/api/v2/parties/", 'GET')
        self.assertEqual(resultGet.status_code, 200)

        dataCheckGet = json.loads(resultGet.data)
        self.check_standard_reply(dataCheckGet, 200)

    def test_update_party_name(self):
        """Tests for Patch Data /api/v2/parties/<int:partyid>"""
        party1c = self.gen_party()
        result12 = self.post('/api/v2/parties', data=party1c)
        dataCheck = json.loads(result12.data)
        patch_data = self.gen_party()
        url = '/api/v2/parties/{}'.format(dataCheck['data']['id'])
        result = self.send_auth_request(url, 'PATCH', data=patch_data)
        self.assertEqual(result.status_code, 202)
        datacheck = json.loads(result.data)
        self.check_standard_reply(datacheck, 202)

    def test_delete_party(self):
        """Tests for [DELETE] /api/v2/parties/<int:partyId>to delete party"""
        party1c = self.gen_party()
        result12 = self.post('/api/v2/parties', data=party1c)
        dataCheck = json.loads(result12.data)

        result = self.send_auth_request(
            "/api/v2/parties/{}".format(dataCheck['data']['id']), 'DELETE')
        self.assertEqual(result.status_code, 200)

        datacheck2 = json.loads(result.data)
        self.check_standard_reply(datacheck2, 200)
        self.assertTrue('message' in datacheck2['data'])

    def gen_party(self):
        return {
            'name': BaseTest().random_name(10),
            'hqAddress': '23 jumpstreet',
            'logoUrl': 'www.url.com/ ' + BaseTest().random_name(10),
        }

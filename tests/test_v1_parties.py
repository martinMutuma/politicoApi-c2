"""app/test/test_v1_party_create.py """

from tests.base_test import BaseTest
import json
class TestParties(BaseTest):
    """ Test endpoints  app/v1/parties """
    party1 =  {
            'name' : 'Party A',
            'hqAddress' : '22 jumpstreet',
            'logoUrl' : 'www.url.com/party.png',
            }
    party2  = {
            'name' : 'Par',
            'hqAddress' : '22 jumpstreet',
            'logoUrl' : 'www.url.com/party.png',
    }
    party3  = {
            'name' : 'Par',
            'logoUrl' : 'www.url.com/party.png',
    }
    def test_create_party(self):
        """ api/v1/parties Post test """
        result = self.client().post('/api/v1/parties', data=self.party1 )
        dataCheck = json.loads(result.data)
        self.assertEqual(result.status_code, 201)
        self.assertTrue('status' in dataCheck)
        self.assertEqual(dataCheck['status'], 201)
        self. assertTrue('data' in dataCheck)
        self.assertTrue('id' in dataCheck['data'])
        self.assertTrue(isinstance(dataCheck['data']['id'], int ))
        self.assertEqual(dataCheck['data']['name'], self.party1['name'])
        
    def test_create_party_with_wrong_data(self):
            """ api/v1/parties Post test with invalid data"""
            result = self.client().post('/api/v1/parties', data=self.party2 )
            dataCheck = json.loads(result.data)
            result2 = self.client().post('/api/v1/parties', data=self.party3 )
            dataCheck2 = json.loads(result.data)

            self.assertEqual(result.status_code, 400)
            self.assertTrue('status' in dataCheck)
            self.assertEqual(dataCheck['status'], 400)
            self.assertTrue('error' in dataCheck)

            self.assertEqual(result2.status_code, 400)
            self.assertTrue('status' in dataCheck2)
            self.assertEqual(dataCheck2['status'], 400)
            self.assertTrue('error' in dataCheck2)
           
            

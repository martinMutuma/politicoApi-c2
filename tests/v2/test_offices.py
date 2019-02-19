"""app/test/test_v1_offices.py """
import json
from tests.v2 import BaseTest


class TestOffices(BaseTest):
    """
    Test endpoints  app/v2/offices
    """
    office1 = {
        'name': BaseTest().random_name(10),
        'type': 'state'
    }

    office1d = {
        'name': BaseTest().random_name(10),
        'type': 'state'
    }

    def test_create_office(self):
        office = self.generate_random_office()

        result = self.send_auth_request("/api/v2/offices", "POST", data=office)
        self.assertEqual(result.status_code, 201)
        dataCheck = json.loads(result.data)
        self.check_standard_reply(dataCheck, 201)

    def test_create_office_missing_field(self):
        office = self.generate_random_office()
        del office['name']
        result = self.send_auth_request("/api/v2/offices", "POST", data=office)
        self.assertEqual(result.status_code, 400)
        dataCheck = json.loads(result.data)
        self.check_standard_reply(dataCheck, 400, True)

    def test_create_office_no_data(self):
        result = self.send_auth_request("/api/v2/offices", "POST")
        self.assertEqual(result.status_code, 400)
        dataCheck = json.loads(result.data)
        self.check_standard_reply(dataCheck, 400, True)

    def test_create_office_duplicate(self):
        self.send_auth_request(
            "/api/v2/offices", "POST", data=self.office1)
        result = self.send_auth_request(
            "/api/v2/offices", "POST", data=self.office1)
        self.assertEqual(result.status_code, 400)
        dataCheck = json.loads(result.data)
        self.check_standard_reply(dataCheck, 400, True)

    def test_get_specific_office_details(self):
        office2 = self.generate_random_office()
        result = self.send_auth_request(
            "/api/v2/offices", "POST", data=office2)
        dataCheck = json.loads(result.data)

        result_get = self.send_auth_request(
            "/api/v2/offices/{}".format(dataCheck['data']['id']), "GET")
        self.assertEqual(result_get.status_code, 200)

        data_check_get = json.loads(result_get.data)
        self.check_standard_reply(data_check_get, 200)
        self.assertEqual(data_check_get['data']['name'], office2['name'])

    def test_get_specif_office_details_office_not_exist(self):
        resultGet1 = self.send_auth_request(
            "/api/v2/offices/2999999", 'GET')
        self.assertEqual(resultGet1.status_code, 404)

        dataCheckGet = json.loads(resultGet1.data)

        self.check_standard_reply(dataCheckGet, 404, True)

    def test_get_all_offices(self):
        office3 = {
            'name': 'Office c',
            'type': 'legislative'
        }
        self.send_auth_request("/api/v2/offices", 'POST', data=office3)
        result_get = self.send_auth_request("/api/v2/offices", 'GET')
        self.assertEqual(result_get.status_code, 200)

        data_check_get = json.loads(result_get.data)
        self.check_standard_reply(data_check_get, 200)

    def test_update_office_name(self):
        """Tests for Patch Data /api/v2/offices/<int:officeid>/"""
        office1d = self.generate_random_office()
        result12 = self.send_auth_request(
            '/api/v2/offices', 'POST', data=office1d)
        dataCheck = json.loads(result12.data)
        patch_data = {'name': self.random_name()}
        url = '/api/v2/offices/{}'.format(dataCheck['data']['id'])
        result = self.send_auth_request(url, 'PATCH', data=patch_data)
        self.assertEqual(result.status_code, 202)
        datacheck = json.loads(result.data)
        self.check_standard_reply(datacheck, 202)
        self.assertEqual(datacheck['data']['name'], patch_data['name'])

    def test_delete_office(self):
        """Tests for [DELETE] /api/v2/offices/<int:officeId>to delete office"""
        office1d = self.generate_random_office()
        result12 = self.send_auth_request(
            '/api/v2/offices', 'POST', data=office1d)
        dataCheck = json.loads(result12.data)
        result = self.send_auth_request(
            "/api/v2/offices/{}".format(dataCheck['data']['id']), 'DELETE')
        self.assertEqual(result.status_code, 200)
        datacheck2 = json.loads(result.data)
        self.check_standard_reply(datacheck2, 200)
        self.assertTrue('message' in datacheck2['data'])

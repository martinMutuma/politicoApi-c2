import json
from tests.v2 import BaseTest


class TestCandidate(BaseTest):
    """Tests for Candidates"""

    def test_create_candidate(self):
        office = self.generate_random_office()
        result2 = self.send_auth_request(
            "/api/v2/offices", "POST", data=office)
        self.assertEqual(result2.status_code, 201)
        dataCheck2 = json.loads(result2.data)
        office_id = dataCheck2['data']['id']
        user = self.generate_user()
        result3 = self.send_auth_request(
            '/api/v2/auth/signup', 'POST', data=user)
        self.assertEqual(result3.status_code, 201)
        datacheck3 = json.loads(result3.data)
        user_id = datacheck3['data']['user']['id']
        candidate = dict(user_id=str(user_id))
        resultC = self.send_auth_request(
            "/api/v2/offices/{}/register".format(office_id), "POST",
            data=candidate)
        self.assertEqual(resultC.status_code, 201)

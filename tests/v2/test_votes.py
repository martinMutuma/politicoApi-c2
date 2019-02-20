import json
from tests.v2 import BaseTest


class TestVotes(BaseTest):
    """Tests for votes"""

    def test_cast_vote(self):

        # exit("at tests")
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
        url = "/api/v2/offices/{}/register".format(office_id)
        resultC = self.send_auth_request(url, "POST", data=candidate)
        self.assertEqual(resultC.status_code, 201)
        candidate_data = json.loads(resultC.data)
        candidate_id = candidate_data['data']['id']
        vote = {'createdBy': user_id,
                'candidate_id': candidate_id, 'office_id': office_id}
        result_vote = self.send_auth_request(
            "/api/v2/votes", "POST", data=vote)
        print(json.loads(result_vote.data))
        self.assertEqual(result_vote.status_code, 201)

    def test_cast_vote_wrong_data(self):
        vote = {'createdBy': 45454545455454545,
                'candidate_id': 545454545454545, 'office_id': 54545545454454}
        result_vote = self.send_auth_request(
            "/api/v2/votes", "POST", data=vote)
        self.assertEqual(result_vote.status_code, 400)

from tests.v2 import BaseTest
from app.v2.models.vote_model import VoteModel


class TestResults(BaseTest):
    """Tests for autn"""

    def test_results(self):
        votes = VoteModel()
        results = votes.get(True)
        office_id = 0
        if results is not None:
            office_id = results['office_id']
        url = '/api/v2/offices/{}/result'.format(office_id)
        get_result = self.send_auth_request(url, 'GET')
        self.assertEqual(get_result.status_code, 200, "Result was not found")

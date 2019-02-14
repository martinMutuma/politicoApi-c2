import json
from tests.v2 import BaseTest


class TestAuth(BaseTest):
    """Tests for autn"""

    def test_auth_signup(self):
        data = self.generate_user()
        result = self.send_auth_request('/api/v2/auth/signup','POST',data)
        self.assertEqual(result.status_code, 201)
        datacheck = json.loads(result.data)
        self.check_standard_reply(datacheck, 201)
        



    def generate_user(self):
        return {
            "email": "email{}@mail.com".format(BaseTest.random_name(4)),
            "password": "password",
            "firstname": "Name",
            "othername": "OtherName",
            "lastname": "Wellname",
            "phonenumber": "0893292992",
            "passporturlstring": "www.url.com/"+BaseTest.random_name(4)
        }

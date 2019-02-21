from tests.v2 import BaseTest
from app.v2.views.validate import Validate


class TestValidate(BaseTest):
    """Tests for validatation class """

    def test_required(self):
        required = ['name', 'age']
        data_submitted = {'name': 'my name', 'age': 45}
        validate = Validate.required(required, data_submitted)
        self.assertEqual(validate['status'], True)

    def test_required_missing(self):
        required = ['name', 'age']
        data_submitted = {'name': 'my name', }
        validate = Validate.required(required, data_submitted)
        self.assertEqual(validate['status'], False)

    def test_validate_name(self):
        name = 'Good name'
        validate = Validate.validate_name(name)
        self.assertEqual(validate['status'], True)

    def test_validate_name_less_two_chars(self):
        name = 'a'
        validate = Validate.validate_name(name)
        self.assertEqual(validate['status'], False)

    def test_validate_name_special_chars(self):
        name = 'a4#$$$$#%%me'
        validate = Validate.validate_name(name)
        self.assertEqual(validate['status'], False)

    def test_validate_url(self):
        url = "www.google.com"
        validate = Validate.validate_url(url)
        self.assertEqual(validate['status'], True)

    def test_validate_url_wrong(self):
        url = "www.google"
        validate = Validate.validate_url(url)
        self.assertEqual(validate['status'], False)

    def test_validate_length(self):
        name = 'my name'
        validate = Validate.validate_length(name)
        self.assertEqual(validate['status'], True)

    def test_validate_length_short(self):
        name = 'my name'
        validate = Validate.validate_length(name, 10)
        self.assertEqual(validate['status'], False)

    def test_validate_email(self):
        email = 'mail@mial.com'
        validate = Validate.validate_email(email)
        self.assertEqual(validate['status'], True)

    def test_validate_email_wron(self):
        email = 'mailmial.com'
        validate = Validate.validate_email(email)
        self.assertEqual(validate['status'], False)

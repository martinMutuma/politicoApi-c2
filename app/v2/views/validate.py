"""
app/v1/views/validate.py
"""

import re
special_chars = r'[0-9~!@#$%^&*()_-`{};:\'"\|/?.>,<]'


class Validate:
    errors = []
    @classmethod
    def required(cls, fields=[], dataDict={}):
        """Checks for a missing submit from a list of required"""
        notFound = []
        if len(fields) > 0:
            notFound = [
                i for i in fields
                if i not in dataDict or len(str(dataDict[i])) < 1
            ]

        if (len(notFound) > 0):
            msg = "Validation error,Following fields are required: {}".format(
                ", ".join(notFound))
            return cls.make_retun_dict(False, msg)

        else:
            return cls.make_retun_dict(True)

    @classmethod
    def validate_name(cls, name):
        """Name validation
        should not contain special characters and len > 3
        """
        name = name.strip()
        print(name)
        if bool(re.search(special_chars, name))is True:
            msg = "Name Should not contain special characters"
            return cls.make_retun_dict(False, msg)
        elif len(name) <= 3:
            msg2 = "Name should be 4  characters and above"
            return cls.make_retun_dict(False, msg2)
        else:
            return cls.make_retun_dict(True)

    @classmethod
    def make_retun_dict(cls, status, message=''):
        """Universal return dictionary for whole
        validation class {message:message , status:status
        """
        return dict(message=message, status=status)

    @classmethod
    def validate_length(cls, name, lenth=3):
        """Validates lenght of a string"""

        if len(name) <= lenth:
            msg = "Should be longer than {}".format(str(lenth))
            return cls.make_retun_dict(False, msg)
        return cls.make_retun_dict(True)

    @classmethod
    def validate_url(cls, Url):
        """
        To validate urls
        Takes url as the parameter

        """
        pattern = r"^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/|www\.)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$"
        if not re.match(pattern, Url):
            return cls.make_retun_dict(False, "Must be a valid Url")
        return cls.make_retun_dict(True, "valid url")

    @classmethod
    def validate_email(cls, mail):
        """Validate Email"""
        pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
        if not re.match(pattern, mail):
            return cls.make_retun_dict(False, "Invalid Email")
        return cls.make_retun_dict(True, "Valid Email")

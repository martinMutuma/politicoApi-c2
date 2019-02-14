"""
app/v1/views/validate.py
"""

import re
from urllib.parse import urlparse
special_chars = r'[0-9~!@#$%^&*()_-`{};:\'"\|/?.>,<]'


class Validate:

    @classmethod
    def required(cls, fields=[], dataDict={}):
        """Checks for a missing submit from a list of required"""
        notFound = []
        if len(fields) > 0:
            notFound = [
                i for i in fields if i not in dataDict or len(dataDict[i]) < 1]

        if (len(notFound) > 0):
            return cls.make_retun_dict(False, "Validation error,Following fields are required: {}".format(", ".join(notFound)))

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
            return cls.make_retun_dict(False, "Name Should not contain special characters")
        elif len(name) <= 3:
            return cls.make_retun_dict(False, "Name should be 4  characters and above")
        else:
            return cls.make_retun_dict(True)

    @classmethod
    def make_retun_dict(cls, status, message=''):
        "Universal return dictionary for whole validation class {message:message , status:status}"
        return dict(message=message, status=status)

    @classmethod
    def validate_length(cls, name, lenth=3):
        """Validates lenght of a string"""

        if len(name) <= lenth:
            return cls.make_retun_dict(False, "Should be longer than {}".format(str(lenth)))
        return cls.make_retun_dict(True)

    @classmethod
    def validate_url(cls, Url):
        """
        To validate urls 
        Takes url as the parameter 

        """
        try:
            result = urlparse(Url)
            if all([result.scheme, result.netloc, result.path]):
                return cls.make_retun_dict(True)
            else:
                return cls.make_retun_dict(False, "Must be a valid Url")
        except:
            return cls.make_retun_dict(False, "Must be a valid Url")

    @classmethod
    def validate_email(cls, mail):
        pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
        if not re.match(pattern, mail):
            return cls.make_retun_dict(False, "Invalid Email")
        return cls.make_retun_dict(True, "Valid Email")

    

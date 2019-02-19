from flask import request, make_response, jsonify, abort
from app.v2.views.validate import Validate


class Views(object):
    """Common functions used by views"""
    errors = []
    @staticmethod
    def get_data():
        '''Getting data from json or form submitted data'''

        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        if not data:
            try:
                data = request.get_json(force=True)
            except Exception as e:
                data = dict()
                Views.errors.append(e)

        for key, value in data.items():
            if type(value) == str:
                data[key] = value.strip()

            data[key] = value

        return data

    @classmethod
    def check_for_required_fields(cls,  fields=[], dataDict={}):
        """Uses validate class to validate
            all required fields exist in the submitted data

        Keyword Arguments:
            fields {list} -- [fieds expected by the function] (default: {[]})
            dataDict {dict} -- [Fields and data submitted by the user]
             (default: {{}})

        Returns:
            [bool] -- [True if all fields exist]
            [httt exit] if any of the fields do not exist
        """

        validateRequired = Validate.required(fields=fields, dataDict=dataDict)
        if validateRequired['status'] is False:
            msg = validateRequired['message']
            res = jsonify(
                {'status': 400, 'error': msg, 'data': []})
            return abort(make_response(res, 400))
        return True

    @staticmethod
    def destroy_db():
        """
        used by when testing incase one wants to
        clean up the data and test a flesh

        """
        return make_response("Done", 200)

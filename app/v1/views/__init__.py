from flask import request, make_response, jsonify, abort
from app.v1.models.political_parties import partiesList
from app.v1.models.office_model import officeList
from app.v1.views.validate import Validate


class Views(object):
    """Common functions used by views"""
    
    @staticmethod
    def get_data():
        '''Getting data from json or form submitted data '''
    
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        if not data:
            try:
                data = request.get_json(force=True)  
            except:
                data = dict() 

        return data

    @classmethod
    def check_for_required_fields(cls,  fields=[], dataDict={}):
        validateRequired = Validate.required(fields=fields, dataDict=dataDict)
        if validateRequired['status'] == False:
            res = jsonify(
                {'status': 400, 'error': validateRequired['message'], 'data': []})
            return abort(make_response(res, 400))
        return True

    @staticmethod
    def destroy_lists():
        partiesList.clear()
        officeList.clear()
        return make_response("Done", 200)
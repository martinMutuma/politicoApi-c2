from flask import request, make_response, jsonify, abort
from app.v2.models.candidate_model import CandidateModel
from app.v2.models.user_model import UserModel
from app.v2.models.office_model import OfficeModel
from app.v2.models.party_model import PartyModel
from app.v2.views import Views
from app.v2.views.validate import Validate
from app.v2.views import auth

@auth.require_auth_admin
def register(office_id):
    """Registeres a candidate into the system"""
    data = Views.get_data()

    required_fields = ['user_id']
    Views.check_for_required_fields(
        fields=required_fields, dataDict=data)

    data['office_id'] = office_id
    user = UserModel()
    error_message = []
    if user.get_one(data['user_id']) is None:
            error_message.append('User Does not exist')

    office = OfficeModel()
    if office.get_one(data['office_id']) is None:
        error_message.append('Office Does not exist')
    candidate = CandidateModel()
    candidate.where(data)
    candidate.get()
    if candidate.id is not None:
        error_message.append('Candidate already exists')
        
    if len(error_message) != 0:
        res = jsonify({'error': ",".join(error_message), "status":400})
        return make_response(res, 400)
    
    save_data = candidate.clean_insert_dict(data, False)
    candidate.insert(save_data)
    if candidate.id is not None:
        data = candidate.sub_set()
        status = 201
        return make_response(jsonify(dict(data=data, status=status)), status)
    return make_response(jsonify({"error": "Could not create Candidate", 'status': 400}), 400)

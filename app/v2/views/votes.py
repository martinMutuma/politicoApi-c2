from flask import request, make_response, jsonify, abort
from app.v2.models.candidate_model import CandidateModel
from app.v2.models.user_model import UserModel
from app.v2.models.office_model import OfficeModel
from app.v2.models.party_model import PartyModel
from app.v2.models.vote_model import VoteModel
from app.v2.views import Views
from app.v2.views.validate import Validate


def vote():
    """Registeres a candidate into the system"""
    data = Views.get_data()

    required_fields = ['createdBy', 'candidate_id','office_id']
    Views.check_for_required_fields(
        fields=required_fields, dataDict=data)

    user = UserModel()
    error_message = []
    if user.get_one(data['createdBy']) is None:
            error_message.append('User Does not exist')

    office = OfficeModel()
    if office.get_one(data['office_id']) is None:
        error_message.append('Office Does not exist')
    candidate = CandidateModel()
    if candidate.get_one(data['candidate_id']) is None:
        error_message.append('Candidate does not exist')
    vote=VoteModel()
    where_data ={'office_id':data['office_id'], 'createdBy':data['createdBy']}
    vote.where(where_data)
    vote.get()
    if vote.id is not None:
        error_message.append('You have already voted for that office')

    if len(error_message) != 0:
        res = jsonify({'error': ",".join(error_message), "status":400})
        return make_response(res, 400)
    
    save_data = vote.clean_insert_dict(data, False)
    vote.insert(save_data)
    if vote.id is not None:
        data = vote.sub_set()
        status = 201
        return make_response(jsonify(dict(data=data, status=status)), status)
    return make_response(jsonify({"error": "Could not create Candidate", 'status': 400}), 400)

from flask import make_response, jsonify, request
from app.v2.models.candidate_model import CandidateModel
from app.v2.models.user_model import UserModel
from app.v2.models.vote_model import VoteModel
from app.v2.models import BaseModel
from app.v2.models.office_model import OfficeModel
from app.v2.views import Views
from app.v2.views import auth

candidate_views_model = BaseModel()
candidate_views_model.create_model('candidate_details', 'candidatev_id')


@auth.require_auth
def vote():
    """Cast vote"""
    data = Views.get_data()
    required_fields = ['candidate_id', 'office_id']
    Views.check_for_required_fields(
        fields=required_fields, dataDict=data)

    user = UserModel()
    data['createdBy'] = request.user.get('id')
    error_message = []
    if user.get_one(data['createdBy']) is None:
        error_message.append('User Does not exist')
    office = OfficeModel()
    if office.get_one(data['office_id']) is None:
        error_message.append('Office Does not exist')
    candidate = CandidateModel()
    candidate.where({'office_id': data['office_id']})
    if candidate.get_one(data['candidate_id']) is None:
        error_message.append('Candidate does not exist for that office')
    vote = VoteModel()
    where_data = {'office_id': data['office_id'],
                  'createdBy': data['createdBy']}
    vote.where(where_data)
    vote.get()
    if vote.id is not None:
        error_message.append('You have already voted for that office')

    if len(error_message) != 0:
        res = jsonify({'error': ",".join(error_message), "status": 400})
        return make_response(res, 400)

    save_data = vote.clean_insert_dict(data, False)
    vote.insert(save_data)
    if vote.id is not None:
        data = vote.sub_set()
        status = 201
        return make_response(jsonify(dict(data=data, status=status)), status)
    res = {"error": "Could not create Candidate", 'status': 400}
    return make_response(jsonify(res), 400)


@auth.require_auth
def get_user_votes():
    data = {}
    data['createdBy'] = request.user.get('id')
    vote_view_model = BaseModel()
    vote_view_model = vote_view_model.create_model('vote_details')
    vote_view_model.where(data)
    votes = vote_view_model.get(False)
    res = {'data': votes, 'status': 200}
    return make_response(jsonify(res), res['status'])


@auth.require_auth
def check_voted(office_id):
    where_data = {'office_id': office_id,
                  'createdBy':  request.user.get('id')}
    vote = VoteModel()
    vote.where(where_data)
    vote.get()
    if vote.id is not None:
        res = {"data": {'voted': True, 'vote': vote.sub_set()}, 'status': 200}
    else:
        res = {"data": {'voted': False, 'vote': {}}, 'status': 200}

    return make_response(jsonify(res), res['status'])

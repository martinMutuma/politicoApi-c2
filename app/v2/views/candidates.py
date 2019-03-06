from flask import make_response, jsonify
from app.v2.models.candidate_model import CandidateModel
from app.v2.models.user_model import UserModel
from app.v2.models.office_model import OfficeModel
from app.v2.models import BaseModel
from app.v2.views import Views
from app.v2.views import auth

candidate_views_model = BaseModel()
candidate_views_model.create_model('candidate_details', 'candidatev_id')


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
    candidate.where({'user_id': data['user_id']})
    candidate.get()
    if candidate.id is not None:
        error_message.append('User already a candidate')

    if len(error_message) != 0:
        res = jsonify({'error': ",".join(error_message), "status": 400})
        return make_response(res, 400)

    save_data = candidate.clean_insert_dict(data, False)
    candidate.insert(save_data)
    if candidate.id is not None:
        data = candidate.sub_set()
        status = 201
        return make_response(jsonify(dict(data=data, status=status)), status)
    res = {"error": "Could not create Candidate", 'status': 400}
    return make_response(jsonify(res), 400)


@auth.require_auth
def get_candidate_details(candidate_id):
    candidate_views_model.where({'candidatev_id': candidate_id})
    candidate_views_model.select()
    candidate = candidate_views_model.get()
    if candidate is not None:
        res = {"status": 200,
               'data': candidate
               }
    else:
        res = {"error": "Candidate not found", 'status': 400}

    return make_response(jsonify(res), res['status'])


@auth.require_auth
def get_candidate_by_user_id(user_id):
    candidate_views_model.where({'candidate_user_id': user_id})
    candidate_views_model.select()
    candidate = candidate_views_model.get()
    if candidate is not None:
        res = {"status": 200,
               'data': candidate
               }
    else:
        res = {"error": "Not a candidate", 'status': 400}

    return make_response(jsonify(res), res['status'])


@auth.require_auth
def get_all_candidates():
    """Get a list of all candidates
    Returns:
        [api response] -- [with all candidates]
    """
    candidate_views_model.select()
    all_candidates = candidate_views_model.get(False)
    res = jsonify({"status": 200,
                   'data': all_candidates
                   })
    return make_response(res, 200)


@auth.require_auth
def get_candidates_by_office(office_id):
    """Get a list of all candidates by office id
    Returns:
        [api response] -- [with all candidates]
    """
    candidate_views_model.where({'candidate_office_id': office_id})
    candidate_views_model.select()
    all_candidates = candidate_views_model.get(False)
    res = jsonify({"status": 200,
                   'data': all_candidates
                   })
    return make_response(res, 200)

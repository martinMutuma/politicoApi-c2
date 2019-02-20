from flask import make_response, jsonify, request
from app.v2.models.candidate_model import CandidateModel
from app.v2.models.petition_model import PetitionModel
from app.v2.views import Views
from app.v2.views import auth


@auth.require_auth
def create_pettion():
    """Cast vote"""
    data = Views.get_data()
    required_fields = ['body', 'evidence']
    Views.check_for_required_fields(
        fields=required_fields, dataDict=data)

    data['createdBy'] = request.user.get('id')
    error_message = []

    candidate = CandidateModel()
    candidate.where(
        {'user_id': data['createdBy']})
    if candidate.get() is None:
        error_message.append('You are not a candidate for that office')
    else:
        data['office_id'] = candidate.office_id
        petition = PetitionModel()
        where_data = {'office_id': data['office_id'],
                      'createdBy': data['createdBy']}
        petition.where(where_data)
        petition.get()
        if petition.id is not None:
            error_message.append(
                'You have a pending petition')

    if len(error_message) != 0:
        res = jsonify({'error': ",".join(error_message), "status": 400})
        return make_response(res, 400)

    save_data = petition.clean_insert_dict(data, False)
    print(save_data)
    petition.insert(save_data)
    if petition.id is not None:
        data = petition.sub_set()
        status = 201
        return make_response(jsonify(dict(data=data, status=status)), status)
    res = {"error": "Could not create Petition ", 'status': 400}
    return make_response(jsonify(res), 400)

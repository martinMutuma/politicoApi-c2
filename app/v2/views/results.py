from flask import make_response, jsonify
from app.v2.models.vote_model import VoteModel
from app.v2.views import auth


@auth.require_auth
def office_results(office_id):

    votes_model = VoteModel()
    query = """SELECT COUNT(*) As result, office_id, candidate_id
                FROM votes WHERE office_id={}
                GROUP BY candidate_id,office_id;""" .format(office_id)
    votes_model.select_query = query
    print(votes_model.select_query)
    result = votes_model.get(False)
    res = jsonify({'data': result, 'status': 2001})
    return make_response(res, 200)

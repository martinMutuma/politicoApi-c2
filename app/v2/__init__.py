
from app.v2.views import results
from app.v2.views import votes
from app.v2.views import candidates
from app.v2.views import auth
from app.v2.views import petition
from app.v2.views.offices import Offices
from app.v2.views.parties import Parties
from flask import Blueprint

v2_app = Blueprint('api_v2', __name__)


# parties module urls
v2_app.add_url_rule('/parties', view_func=Parties.post_party, methods=['POST'])
v2_app.add_url_rule('/parties/<int:partyId>',
                    view_func=Parties.get_party_details, methods=['GET'])
v2_app.add_url_rule(
    '/parties/', view_func=Parties.get_all_parties, methods=['GET'])
v2_app.add_url_rule('/parties/<int:partyId>',
                    view_func=Parties.update_party_details, methods=['PATCH'])
v2_app.add_url_rule('/parties/<int:partyId>',
                    view_func=Parties.delete_party, methods=['DELETE'])


# office  module Urls
v2_app.add_url_rule(
    '/offices', view_func=Offices.create_office, methods=['POST'])
v2_app.add_url_rule('/offices/<int:office_id>',
                    view_func=Offices.get_details, methods=['GET'])
v2_app.add_url_rule(
    '/offices', view_func=Offices.get_all_offices, methods=['GET'])
v2_app.add_url_rule('/offices/<int:office_id>',
                    view_func=Offices.update_office_details, methods=['PATCH'])
v2_app.add_url_rule('/offices/<int:office_id>',
                    view_func=Offices.delete_office, methods=['DELETE'])
v2_app.add_url_rule('/offices/<int:office_id>/register',
                    view_func=candidates.register, methods=['POST'])
# result route
v2_app.add_url_rule('/offices/<int:office_id>/result',
                    view_func=results.office_results, methods=['get'])

# auth routes
v2_app.add_url_rule('/auth/login', view_func=auth.login, methods=['POST'])
v2_app.add_url_rule('/auth/signup', view_func=auth.signup, methods=['POST'])
v2_app.add_url_rule('/auth/users', view_func=auth.get_users, methods=['GET'])
v2_app.add_url_rule('/auth/admin/<int:user_id>',
                    view_func=auth.make_admin, methods=['PATCH'])

# votes votes
v2_app.add_url_rule('/votes', view_func=votes.vote, methods=['POST'])
# candidates
v2_app.add_url_rule(
    '/candidates', view_func=candidates.get_all_candidates, methods=['GET'])
# candidates
v2_app.add_url_rule(
    '/petitions', view_func=petition.create_pettion, methods=['POST'])

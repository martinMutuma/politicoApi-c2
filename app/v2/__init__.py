"""app/vi/__init__.py"""
from flask import Blueprint

v2_app = Blueprint('api_v2', __name__)

from app.v2.views.parties import Parties

from app.v2.views.offices import Offices
from app.v2.views import  auth

from app.v2.views import Views

#parties module urls
v2_app.add_url_rule('/parties',view_func=Parties.post_party, methods=['POST'])
v2_app.add_url_rule('/parties/<int:partyId>',view_func=Parties.get_party_details, methods=['GET'])
v2_app.add_url_rule('/parties/',view_func=Parties.get_all_parties, methods=['GET'])
v2_app.add_url_rule('/parties/<int:partyId>',view_func=Parties.update_party_details, methods=['PATCH'])
v2_app.add_url_rule('/parties/<int:partyId>',view_func=Parties.delete_party, methods=['DELETE'])


#office  module Urls 
v2_app.add_url_rule('/offices',view_func=Offices.create_office, methods=['POST'])
v2_app.add_url_rule('/offices/<int:office_id>',view_func=Offices.get_details, methods=['GET'])
v2_app.add_url_rule('/offices',view_func=Offices.get_all_offices, methods=['GET'])
v2_app.add_url_rule('/offices/<int:office_id>',view_func=Offices.update_office_details, methods=['PATCH'])
v2_app.add_url_rule('/offices/<int:office_id>',view_func=Offices.delete_office, methods=['DELETE'])

#auth routes 
v2_app.add_url_rule('/auth/login',view_func=auth.login, methods=['POST'])
v2_app.add_url_rule('/auth/signup',view_func=auth.signup, methods=['POST'])
v2_app.add_url_rule('/auth',view_func=auth.test, methods=['POST'])


#Clear data 
v2_app.add_url_rule('/d', view_func=Views.destroy_db )

 
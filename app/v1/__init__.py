"""app/vi/__init__.py"""
from flask import Blueprint

v1_app = Blueprint('api_v1', __name__)

from app.v1.views.parties import Parties

from app.v1.views.offices import Offices

#parties module urls
v1_app.add_url_rule('/parties',view_func=Parties.post_party, methods=['POST'])
v1_app.add_url_rule('/parties/<int:partyId>',view_func=Parties.get_party_details, methods=['GET'])
v1_app.add_url_rule('/parties/',view_func=Parties.get_all_parties, methods=['GET'])
v1_app.add_url_rule('/parties/<int:partyId>/name',view_func=Parties.update_party_details, methods=['PATCH'])
v1_app.add_url_rule('/parties/<int:partyId>',view_func=Parties.delete_party, methods=['DELETE'])


#office  module Urls 
v1_app.add_url_rule('/offices',view_func=Offices.create_party, methods=['POST'])
v1_app.add_url_rule('/offices/<int:office_id>',view_func=Offices.get_details, methods=['GET'])


 
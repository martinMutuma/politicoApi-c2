"""app/vi/__init__.py"""
from flask import Blueprint

v1_app = Blueprint('api_v1', __name__)

from app.v1.views.parties import post_party, get_party_details, get_all_parties

#parties module urls
v1_app.add_url_rule('/parties',view_func=post_party, methods=['POST'])
v1_app.add_url_rule('/parties/<int:partyId>',view_func=get_party_details, methods=['GET'])
v1_app.add_url_rule('/parties/',view_func=get_all_parties, methods=['GET'])


 
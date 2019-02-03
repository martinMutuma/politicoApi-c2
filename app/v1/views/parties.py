"""app/v1/views/parties.py """

from app import polApp
from flask import request

parties = {}
@polApp.route('api/vi/parties',methods=['POST'])
def post_party():
    """ Party data """
    

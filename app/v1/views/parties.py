"""app/v1/views/parties.py """

from app import polApp
from flask import request, make_response, jsonify
from app.v1.views.validate import Validate
partiesList = {}

@polApp.route('/api/v1/parties', methods=['POST'])  
def post_party():
    """ Party data """
    data = get_data()
    validateRequired = Validate.required(fields=['name','hqAddress','logoUrl'], dataDict=data) 
    if validateRequired == True:
        party = create_party(data['name'], data['hqAddress'], data['logoUrl'])
        returnPartydetails ={'name':party['name'], 'id':party['id']}
        res = jsonify({"status":201, 'data':returnPartydetails})
        return make_response(res, 201)
    else:
        res = jsonify({'status':400, 'error':validateRequired, 'data':[]})
        return make_response(res, 400)




    
def create_party(name, hqAddress,logoUrl):
    """Central place to create party for uniformity"""
    partyid = len(partiesList)-1
    newParty = dict(id=partyid, name=name ,hqAddress=hqAddress, logoUrl=logoUrl)
    partiesList[partyid] = newParty
    return newParty

def get_data():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    return data
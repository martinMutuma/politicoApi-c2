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
    if validateRequired['status'] == False:
        res = jsonify({'status':400, 'error':validateRequired['message'], 'data':[]})
        return make_response(res, 400)


    validateName = Validate.validate_name(data['name'])
    if validateName['status'] == False:
        res = jsonify({'status':400, 'error':validateName['message'], 'data':[]})
        return make_response(res, 400)

    validateAddressLen = Validate.validate_length(data['hqAddress'] , 5)
    if validateAddressLen['status'] == False:
        res = jsonify({'status':400, 'error':"hqAddress "+validateAddressLen['message'], 'data':[]})
        return make_response(res, 400)

    # validateLogoUrl = Validate.validate_url(data['logoUrl'])
    # if validateLogoUrl['status'] == False:
    #         res = jsonify({'status':400, 'error':"logoUrl "+validateLogoUrl['message'], 'data':[]})
    #         return make_response(res, 400)

    party = create_party(data['name'], data['hqAddress'], data['logoUrl'])
    returnPartydetails ={'name':party['name'], 'id':party['id']}
    res = jsonify({"status":201, 'data':returnPartydetails})
    return make_response(res, 201)
    
       




    
def create_party(name, hqAddress,logoUrl):
    """Central place to create party for uniformity"""
    #validation 
    
    partyid = len(partiesList)+1
    newParty = dict(id=partyid, name=name ,hqAddress=hqAddress, logoUrl=logoUrl)
    partiesList[partyid] = newParty
    return newParty

def get_data():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    return data
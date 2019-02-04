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
    
       
@polApp.route('/api/v1/parties/<partyId>', methods=['GET'])  
def get_party_details(partyId):
    """Get the details of a specific party"""
    create_partylist()
   
    if len(partiesList) == 0:
        pass #imprement for empty list
    if partyId in partiesList:
        returnPartydetails ={
            'name':partiesList[partyId]['name'], 
            'id':partiesList[partyId]['id'],
            'logoUrl':partiesList[partyId]['logoUrl']
            }
        res = jsonify({"status":200, 'data':returnPartydetails})
        return make_response(res, 200)
    else:
        res = jsonify({"status":404, 'error':"Party with id {} not found".format(partyId)})
        return make_response(res, 404)


    
def create_party(name, hqAddress,logoUrl):
    """Central place to create party for uniformity"""
    #validation 
    
    partyid = len(partiesList)+1
    newParty = dict(id=partyid, name=name ,hqAddress=hqAddress, logoUrl=logoUrl)
    partiesList[partyid] = newParty
    return newParty

def get_data():
    '''Getting data from json or form submitted data '''
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    return data

def create_partylist():
     party1 =  {
                'id':'1',
                'name' : 'Party A',
                'hqAddress' : '22 jumpstreet',
                'logoUrl' : 'www.url.com/party.png',
                }
     partiesList['1']=party1
     return partiesList

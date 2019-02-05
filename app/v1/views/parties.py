"""app/v1/views/parties.py """
import copy
from app.v1 import v1_app
from flask import request, make_response, jsonify
from app.v1.views.validate import Validate
partiesList = {}

# @v1_app.route('/parties', methods=['POST'])


def post_party():
    """ Party data """
    data = get_data()

    validateRequired = Validate.required(
        fields=['name', 'hqAddress', 'logoUrl'], dataDict=data)
    if validateRequired['status'] == False:
        res = jsonify(
            {'status': 400, 'error': validateRequired['message'], 'data': []})
        return make_response(res, 400)

    validateName = Validate.validate_name(data['name'])
    if validateName['status'] == False:
        res = jsonify(
            {'status': 400, 'error': validateName['message'], 'data': []})
        return make_response(res, 400)
    
    validateAddressLen = Validate.validate_length(data['hqAddress'], 5)
    if validateAddressLen['status'] == False:
        res = jsonify({'status': 400, 'error': "hqAddress " +
                       validateAddressLen['message'], 'data': []})
        return make_response(res, 400)

    # validateLogoUrl = Validate.validate_url(data['logoUrl'])
    # if validateLogoUrl['status'] == False:
    #         res = jsonify({'status':400, 'error':"logoUrl "+validateLogoUrl['message'], 'data':[]})
    #         return make_response(res, 400)
    
    party_name_exists = check_name_exists(data['name'])
    if party_name_exists:
        pass
        # res = jsonify({'status': 400, 'error': "Duplicate name error, Party {} already exists with id {}".format(
        #     data['name'], party_name_exists), 'data': []})
        # return make_response(res, 400)

    party = create_party(data['name'], data['hqAddress'], data['logoUrl'])
  

    returnPartydetails = {'name': party['name'], 'id': party['id']}
    res = jsonify({"status": 201, 'data': returnPartydetails})
    return make_response(res, 201)


# @v1_app.route('/parties/<partyId>', methods=['GET'])
def get_party_details(partyId):
    """Get the details of a specific party"""
    if len(partiesList) == 0:
        pass  # imprement for empty list
    if partyId in partiesList:
        returnPartydetails = {
            'name': partiesList[partyId]['name'],
            'id': partiesList[partyId]['id'],
            'logoUrl': partiesList[partyId]['logoUrl']
        }
        res = jsonify({"status": 200, 'data': returnPartydetails})
        return make_response(res, 200)

    res = jsonify(
        {"status": 404, 'error': "Party with id {} not found".format(partyId)})
    return make_response(res, 404)


def get_all_parties():
    """Lists all parties"""
    sub_list = copy.deepcopy(partiesList)
    if len(sub_list) > 0:
        for i in sub_list:
            del sub_list[i]['hqAddress']
    return_parties = [sub_list[i] for i in sub_list]
    res = jsonify({"status": 200, 'data': return_parties})
    return make_response(res, 200)


def create_party(name, hqAddress, logoUrl, partyid=0):
    """Central place to create party for uniformity"""
    if partyid == 0:
        partyid = len(partiesList)+1

    if partyid in partiesList:
        return create_party(name, hqAddress, logoUrl, partyid+1)

    partiesList[partyid]  = dict(id=partyid, name=name,
                    hqAddress=hqAddress, logoUrl=logoUrl)
    return partiesList[partyid] 


def update_party_details(partyId):
    patch_data = get_data()

    validateRequired = Validate.required(
        fields=['name'], dataDict=patch_data)

    if validateRequired['status'] == False:
        res = jsonify(
            {'status': 400, 'error': validateRequired['message'], 'data': []})
        return make_response(res, 400)
     
    party_name_exists = check_name_exists(patch_data['name'])
    if party_name_exists:
        res = jsonify({'status': 400, 'error': "Duplicate name error, Party {} already exists with id {}".format(
            patch_data['name'], party_name_exists), 'data': []})
        return make_response(res, 400)
        
    if partyId in partiesList:
        partiesList[partyId]['name'] = patch_data['name']

        if 'hqAddress' in patch_data:
            partiesList[partyId]['hqAddress'] = patch_data['hqAddress']
        if 'logoUrl' in patch_data:
            partiesList[partyId]['logoUrl'] = patch_data['logoUrl']

        res = {"status":202, "data":{"id":partiesList[partyId]['id'],'name':partiesList[partyId]['name']}}
        return make_response(jsonify(res), 202) #Accepted
   
    res = jsonify(
        {"status": 404, 'error': "Party with id {} not found".format(partyId)})
    return make_response(res, 404)


def delete_party(partyId):
    """Delete Party from list of Parties"""
    if partyId in partiesList:
        deleted_party = partiesList[partyId]
        del partiesList[partyId]
        res = {
            'status':200, 
            'data':{'message':"Party {} deleted".format(deleted_party['name'])}
            }
        return make_response(jsonify(res), 200)

    res = jsonify(
        {"status": 404, 'error': "Party with id {} not found".format(partyId)})
    return make_response(res, 404)


def get_data():
    '''Getting data from json or form submitted data '''
  
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    if not data:
        try:
            data = request.get_json(force=True)  
        except:
            data = dict() 

    return data


def check_name_exists(name):
    """Checks if party Name exists in the parties list"""
    for i in partiesList:
        if name in partiesList[i].values():
            return i
    return False
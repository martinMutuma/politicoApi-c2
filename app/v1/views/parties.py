"""app/v1/views/parties.py """
import copy
# from app.v1 import v1_app
from flask import request, make_response, jsonify
from app.v1.views.validate import Validate
from app.v1.views import Views
from app.v1.models.political_parties import PartyModel, partiesList



class Parties(Views):
   
    @classmethod
    def post_party(cls):
        """ Party data """
        data = Views.get_data()

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

        party = None
        party = PartyModel(data['name'], data['hqAddress'], data['logoUrl'])
        party_name_exists =party.check_name_exists()
        if party_name_exists:
            # pass
            res = jsonify({'status': 400, 'error': "Duplicate name error, Party {} already exists with id {}".format(
                data['name'], party_name_exists), 'data': []})
            return make_response(res, 400)
       
        party.save_party()
        returnPartydetails = party.name_and_id()
        res = jsonify({"status": 201, 'data': returnPartydetails})
        return make_response(res, 201)


    # @v1_app.route('/parties/<partyId>', methods=['GET'])
    @classmethod
    def get_party_details(cls, partyId):
        """Get the details of a specific party"""
        if len(partiesList) == 0:
            pass  # imprement for empty list
        if partyId in partiesList:
            returnPartydetails = partiesList[partyId].get_details()
            res = jsonify({"status": 200, 'data': returnPartydetails})
            return make_response(res, 200)

        res = jsonify(
            {"status": 404, 'error': "Party with id {} not found".format(partyId)})
        return make_response(res, 404)


    @classmethod
    def get_all_parties(cls):
        """Lists all parties"""
        res = jsonify({"status": 200,
                        'data': [partiesList[i].get_details() for i in partiesList]
                        })
        return make_response(res, 200)


    @classmethod
    def update_party_details(cls,partyId):
        patch_data = Views.get_data()

        validateRequired = Validate.required(
            fields=['name'], dataDict=patch_data)

        if validateRequired['status'] == False:
            res = jsonify(
                {'status': 400, 'error': validateRequired['message'], 'data': []})
            return make_response(res, 400)
             
        if partyId in partiesList:
            party_name_exists = partiesList[partyId].check_name_exists(patch_data['name'])
            if party_name_exists:
                res = jsonify({'status': 400, 'error': "Duplicate name error, Party {} already exists with id {}".format(
                    patch_data['name'], party_name_exists), 'data': []})
                return make_response(res, 400)
           
            partiesList[partyId].update_name(patch_data['name'])
            res = {"status":202, "data":partiesList[partyId].name_and_id()}
            return make_response(jsonify(res), 202) #Accepted
    
        res = jsonify(
            {"status": 404, 'error': "Party with id {} not found".format(partyId)})
        return make_response(res, 404)


    @classmethod
    def delete_party(cls, partyId):
        """Delete Party from list of Parties"""
        if partyId in partiesList:
            deleted_party = partiesList[partyId]
            partiesList[partyId].delete_party()
            res = {
                'status':200, 
                'data':{'message':"Party {} deleted".format(deleted_party.name)}
                }
            return make_response(jsonify(res), 200)

        res = jsonify(
            {"status": 404, 'error': "Party with id {} not found".format(partyId)})
        return make_response(res, 404)


"""app/v1/views/parties.py """
import copy
from flask import request, make_response, jsonify, abort
from app.v1.views.validate import Validate
from app.v1.views import Views
from app.v1.models.political_parties import PartyModel, partiesList


class Parties(Views):

    @classmethod
    def post_party(cls):
        """ Party data """
        data = Views.get_data()
        required_fields = ['name', 'hqAddress', 'logoUrl']
        cls.check_for_required_fields(fields=required_fields, dataDict=data)
        cls.validate_party_name(data['name'])
        validateAddressLen = Validate.validate_length(data['hqAddress'], 5)
        if validateAddressLen['status'] == False:
            res = jsonify({'status': 400, 'error': "hqAddress " +
                           validateAddressLen['message'], 'data': []})
            return make_response(res, 400)
        party = None
        party = PartyModel(data['name'], data['hqAddress'], data['logoUrl'])

        party.save_party()
        returnPartydetails = party.name_and_id()
        res = jsonify({"status": 201, 'data': returnPartydetails})
        return make_response(res, 201)

    
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
    def update_party_details(cls, partyId):
        """update party details (impremented name update only)
        
        Arguments:
            partyId {int} -- The Party id to upate
        
        Returns:
            Returns a http response-- depenfing on the actions taken
        """

        patch_data = Views.get_data()

        cls.check_for_required_fields(fields=['name'], dataDict=patch_data)
        cls.validate_party_name(patch_data['name'])

        if partyId in partiesList:
            partiesList[partyId].update_name(patch_data['name'])
            res = {"status": 202, "data": partiesList[partyId].name_and_id()}
        else:
                res = jsonify(
            {"status": 404, 'error': "Party with id {} not found".format(partyId)})
        return make_response(jsonify(res), res['status'])

    @classmethod
    def delete_party(cls, partyId):
        """Delete Party from list of Parties"""
        if partyId in partiesList:
            deleted_party = partiesList[partyId]
            partiesList[partyId].delete_party()
            res = {
                'status': 200,
                'data': {'message': "Party {} deleted".format(deleted_party.name)}
            }
            return make_response(jsonify(res), 200)

        res = jsonify(
            {"status": 404, 'error': "Party with id {} not found".format(partyId)})
        return make_response(res, 404)

   

    @classmethod
    def validate_party_name(cls, name):
        validateName = Validate.validate_name(name)
        if validateName['status'] == False:
            res = jsonify(
                {'status': 400, 'error': validateName['message'], 'data': []})
            abort(make_response(res, 400))
        for party_id in partiesList:
            if partiesList[party_id].name == name:
                res = jsonify({'status': 400, 'error': "Duplicate name error, Party {} already exists with id {}".format(
                    name, party_id), 'data': []})
                abort(make_response(res, 400))
        return True

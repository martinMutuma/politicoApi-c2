"""app/v1/views/parties.py """
import copy
from flask import request, make_response, jsonify, abort
from app.v2.views.validate import Validate
from app.v2.views import Views
from app.v2.models.party_model import PartyModel
from app.v2.views import auth

partiesList = []


class Parties(Views):
    @auth.require_auth
    @classmethod
    def post_party(cls):
        """ Party data """
        data = Views.get_data()
        required_fields = ['name', 'hqAddress', 'logoUrl']
        cls.check_for_required_fields(fields=required_fields, dataDict=data)
        cls.validate_party_name_logo_url(data['name'], data['logoUrl'])
        validateAddressLen = Validate.validate_length(data['hqAddress'], 5)
        if validateAddressLen['status'] == False:
            res = jsonify({'status': 400, 'error': "hqAddress " +
                           validateAddressLen['message'], 'data': []})
            return make_response(res, 400)
        party = None
        party = PartyModel()
        party.create(data['name'], data['hqAddress'], data['logoUrl'])
        save_data = party.clean_insert_dict(data,  full=False)
        party.insert(save_data)
        returnPartydetails = party.sub_set(['name', 'id'])
        res = jsonify({"status": 201, 'data': returnPartydetails})
        return make_response(res, 201)

    @classmethod
    def get_party_details(cls, partyId):
        """Get the details of a specific party"""
        party = PartyModel()
        party_exists = party.get_one(partyId)
        if party_exists is not None:
            returnPartydetails = party.sub_set()
            res = jsonify({"status": 200, 'data': returnPartydetails})
            return make_response(res, 200)

        res = jsonify(
            {"status": 404, 'error': "Party with id {} not found".format(partyId)})
        return make_response(res, 404)

    @classmethod
    def get_all_parties(cls):
        """Lists all parties"""
        party_model = PartyModel()
        select_cols = party_model.sub_set_cols
        party_model.select(select_cols)
        all_parties = party_model.get(False)
        res = jsonify({"status": 200,
                       'data': all_parties
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
        cls.validate_party_name_logo_url(patch_data['name'])
        party = PartyModel()
        party_exists = party.get_one(partyId)
        if party_exists is not None:
            update_data = party.clean_insert_dict(patch_data, False)
            party.update(update_data, partyId)
            print(party.__dict__)
            res = {"status": 202, "data": party.sub_set()}
        else:
            res = jsonify(
                {"status": 404, 'error': "Party with id {} not found".format(partyId)})
        return make_response(jsonify(res), res['status'])

    @classmethod
    def delete_party(cls, partyId):
        """Delete Party from list of Parties"""
        party = PartyModel()
        party_exists = party.get_one(partyId)
        if party_exists is not None:
            party.delete(partyId)
            res = {
                'status': 200,
                'data': {'message': "Party {} deleted".format(party.name)}
            }
            return make_response(jsonify(res), 200)

        res = jsonify(
            {"status": 404, 'error': "Party with id {} not found".format(partyId)})
        return make_response(res, 404)

    @classmethod
    def validate_party_name_logo_url(cls, name, logoUrl=None):
        validateName = Validate.validate_name(name)
        if validateName['status'] == False:
            res = jsonify(
                {'status': 400, 'error': validateName['message'], 'data': []})
            abort(make_response(res, 400))
        party = PartyModel()
        party.where(dict(name=name))
        if party.check_exist() is True:
            res = jsonify({'status': 400, 'error': "Duplicate name error, Party {} already exists with id {}".format(
                name, party.id), 'data': []})
            abort(make_response(res, 400))

        if logoUrl is not None:
            party2 = PartyModel()

            party2.where(dict(logoUrl=logoUrl))
            if party2.check_exist() is True:
                res = jsonify({'status': 400, 'error': "Duplicate logoUrl error, Party  {} already exists with logo {}".format(
                    party2.name, logoUrl), 'data': []})
                abort(make_response(res, 400))
        return True
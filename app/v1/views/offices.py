"""app/v1/views/offices.py """
import copy
# from app.v1 import v1_app
from flask import request, make_response, jsonify
from app.v1.views.validate import Validate
from app.v1.views import Views
from app.v1.models.office_model import OfficeModel, officeList, officeTypes


class Offices(Views):
    """All Control for office Routes"""

    @staticmethod
    def create_office():
        post_data = Views.get_data()

        Views.check_for_required_fields(
            fields=['name', 'type'], dataDict=post_data)

        validateName = Validate.validate_name(post_data['name'])
        if validateName['status'] == False:
            res = jsonify(
                {'status': 400, 'error': validateName['message'], 'data': []})
            return make_response(res, 400)

        if not Offices.validate_type(post_data['type']):
            res = jsonify({'status': 400,
                           'error': "Field type should be one of {}".format(", ".join(officeTypes)),
                           'data': post_data
                           })
            return make_response(res, 400)

        new_office = None
        new_office = OfficeModel(post_data['name'], post_data['type'])
        name_exists = OfficeModel.check_name_exists(
            officeList, new_office.name)
        if name_exists:
            # pass
            res = jsonify({'status': 400, 'error': "Duplicate name error, Office {} already exists with id {}".format(
                post_data['name'], name_exists), 'data': []})
            return make_response(res, 400)
        new_office.save_office()
        return make_response(jsonify({"status": 201, 'data': new_office.get_details()}), 201)

    @staticmethod
    def validate_type(type):
        """Checks if the type of party submitted by the user is one of the predetermined types

        Arguments:
            type {[string]} 

        Returns:
            [Bool] -- [True if it is in the list of accepted types and false if otherwise]
        """

        types_upper = [i.upper() for i in officeTypes]
        if type.upper() in types_upper:
            return True
        return False

    @staticmethod
    def get_details(office_id):
        """ Gets the deails of a specific party
        
        Arguments:
            office_id {[int]} 
        
        Returns:
            [Http response]
        """

        office = OfficeModel.search_office_by_id(office_id)
        print(office)
        if office:
            return make_response(jsonify(
                {'status': 200, 'data': office.get_details()}
            ), 200)

        return make_response(jsonify(
            {'status': 404,
                "error": 'Office with id {} not found'.format(office_id)}
        ))

    @classmethod
    def get_all_offices(cls):
        """Lists all Offices"""
        res = {"status": 200, 'data': [
            officeList[i].get_details() for i in officeList]}
        return make_response(jsonify(res), res['status'])

    @classmethod
    def update_office_details(cls, office_id):
        """A Function that serves edit office endpoint 

        Arguments:
            office_id {[int]} -- [office id to be edited]

        """

        patch_data = Views.get_data()

        cls.check_for_required_fields(fields=['name'], dataDict=patch_data)
        if office_id in officeList:
            ##
            officeList[office_id].update(patch_data['name'])

            res = {"status": 202, "data": officeList[office_id].get_details()}
            return make_response(jsonify(res), 202)  # Accepted

        res = jsonify(
            {"status": 404, 'error': "Office with id {} not found".format(office_id)})
        return make_response(res, 404)

    @classmethod
    def delete_office(cls, office_id):
        """Delete office from list of offices"""
        if office_id in officeList:
            deleted_office = officeList[office_id]
            officeList[office_id].delete()
            res = {'status': 200,
                   'data': {'message': "Office {} deleted".format(deleted_office.name)}
                   }
        else:
            res = {"status": 404,
                   'error': "Office with id {} not found".format(office_id)}
        return make_response(jsonify(res), res['status'])

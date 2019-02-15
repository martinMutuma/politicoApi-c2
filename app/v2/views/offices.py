"""app/v1/views/offices.py """
import copy
# from app.v1 import v1_app
from flask import request, make_response, jsonify, abort
from app.v2.views.validate import Validate
from app.v2.views import Views
from app.v2.models.office_model import OfficeModel,  officeTypes
from app.v2.views import auth

officeList =[]
class Offices(Views):
    """All Control for office Routes"""
   
    @staticmethod
    @auth.require_auth_admin
    def create_office():
        post_data = Views.get_data()
        
        Views.check_for_required_fields(
            fields=['name', 'type'], dataDict=post_data)

        validateName = Validate.validate_name(post_data['name'])
        
        if validateName['status'] == False:
            res = jsonify(
                {'status': 400, 'error': validateName['message'], 'data': []})
            return make_response(res, 400)
        
        if  Offices.validate_type(post_data['type']) is not True:
            res = jsonify({'status': 400,
                           'error': "Field type should be one of {}".format(", ".join(officeTypes)),
                           'data': post_data
                           })
            return make_response(res, 400)

        new_office = None
        new_office = OfficeModel()
        new_office.create_office(post_data['name'], post_data['type'])
        new_office.where(dict(name=post_data['name']))
        if new_office.check_exist() is True:
            # pass
            res = jsonify({'status': 400, 'error': "Duplicate name error, Office {} already exists with id {}".format(
                post_data['name'], new_office.id), 'data': []})
            return make_response(res, 400)
        print("office does not exist")
        insert_data=new_office.clean_insert_dict(post_data,False)
        new_office.insert(insert_data)
        print(new_office.__dict__)
        return make_response(jsonify({"status": 201, 'data': new_office.sub_set()}), 201)

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
    @auth.require_auth
    def get_details(office_id):
        """ Gets the deails of a specific party
        
        Arguments:
            office_id {[int]} 
        
        Returns:
            [Http response]
        """

        office = OfficeModel()
        office_exists=office.get_one(office_id)
        print(office)
        if office_exists is not None:
            return make_response(jsonify(
                {'status': 200, 'data': office.sub_set()}
            ), 200)

        return make_response(jsonify(
            {'status': 404,
                "error": 'Office with id {} not found'.format(office_id)}
        ))

    @classmethod
    @auth.require_auth
    def get_all_offices(cls):
        """Lists all Offices"""
        office_model = OfficeModel()
        office_model.select(office_model.sub_set_cols)
        all_offices = office_model.get(False)
        res = {"status": 200, 'data': all_offices }
        return make_response(jsonify(res), res['status'])

    @classmethod
    @auth.require_auth_admin
    def update_office_details(cls, office_id):
        """A Function that serves edit office endpoint 

        Arguments:
            office_id {[int]} -- [office id to be edited]

        """

        patch_data = Views.get_data()

        cls.check_for_required_fields(fields=['name'], dataDict=patch_data)
        cls.validate_office_name(patch_data['name'])
        office = OfficeModel()
        office_exists = office.get_one(office_id)
        if office_exists is not None:
            ##
            update_data= office.clean_insert_dict(patch_data, False)
            office.update(update_data, office_id)

            res = {"status": 202, "data": office.sub_set()}
            return make_response(jsonify(res), 202)  # Accepted

        res = jsonify(
            {"status": 404, 'error': "Office with id {} not found".format(office_id)})
        return make_response(res, 404)

    @classmethod
    @auth.require_auth_admin
    def delete_office(cls, office_id):
        """Delete office from list of offices"""
        office= OfficeModel()
        exist = office.get_one(office_id)
        if exist is not None:
            office.delete(office_id)
            
            res = {'status': 200,
                   'data': {'message': "Office {} deleted".format(office.name)}
                   }
        else:
            res = {"status": 404,
                   'error': "Office with id {} not found".format(office_id)}
        return make_response(jsonify(res), res['status'])

    @classmethod
    def validate_office_name(cls, name):
        office_model = OfficeModel()
        office_model.where(dict(name=name))
        if office_model.check_exist() is True:
            res = jsonify({'status': 400, 'error': "Duplicate name error, Office {} already exists with id {}".format(
                name, office_model.id), 'data': []})
            abort(make_response(res, 400))



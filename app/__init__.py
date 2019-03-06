"""
app/__init__.py
"""

import os
import string
import random
from flask import Flask, make_response, jsonify
from instance.config import configs
from app.v1 import v1_app
from app.v2 import v2_app
from app.db_setup import DbSetup
from app.v2.models.user_model import UserModel
from app.v2.views.auth import hash_password


#  polApp = create_app()


def create_app(config='development'):
    """Creates the app object and attacges all neccessary urls

    Keyword Arguments:
        config {str} -- [Config to use to create the app]
         (default: {'development'})

    Returns:
        [object] -- [Flask instance]
    """

    app = Flask(__name__)

    app.config.from_object(configs[config])

    app.register_blueprint(v1_app, url_prefix='/api/v1')
    app.register_blueprint(v2_app, url_prefix='/api/v2')
    db = DbSetup(config)
    with app.app_context():
        db.create_tables()

    create_default_admin()
    if (config == 'development'):
        seed_users(10)

    @app.route('/routes', methods=['GET'])
    def home():
        """Default Home route when you load the app"""
        routes = []
        for route in app.url_map.iter_rules():
            routes.append(str(route))
        res = dict(
            endpoints=routes,
            message="Welcome to Polical by Martin",
            status=200,
        )
        return make_response(jsonify(res), 200)

    @app.errorhandler(404)
    def endpoint_not_found(*args):
        """Handles all error 404 responses
            For compliance with API endpoint standard replies n]
        """

        res = dict(
            error="Endpoint not found",
            status=404
        )
        return make_response(jsonify(res), 404)

    @app.errorhandler(500)
    def endpoint_server_error(*args):
        """ Handles server errors
        """

        res = {
            "error": "Its not you, its us",
            "status": 500
        }
        return make_response(jsonify(res), 500)

    @app.errorhandler(405)
    def method_not_allowed(*args):
        """
        Handles method not allowed erros

        """

        res = jsonify(dict(
            error="Method not allowed",
            status=405
        ))
        return make_response(res, 405)

    return app


def create_default_admin():
    """Creates the default admin for the application
    """

    user = None
    user = UserModel()
    email = os.getenv('ADMIN_EMAIL')
    firstname = os.getenv('ADMIN_FIRST_NAME')
    lastname = os.getenv('ADMIN_LAST_NAME')
    password = os.getenv('ADMIN_PASSWORD')
    passporturlstring = os.getenv('ADMIN_PASSPORT')
    default_admin = dict(firstname=firstname, lastname=lastname,
                         email=email, password=password, isAdmin=True,
                         passporturlstring=passporturlstring)
    if email is not None:
        user.where(dict(email=default_admin['email']))
        if user.check_exist() is not True:
            save_data = user.clean_insert_dict(default_admin,  full=False)
            save_data['password'] = hash_password(default_admin['password'])
            user.insert(save_data)


def seed_users(n=10):
    x = 0
    users = None
    users = UserModel()
    print("User Count:", users.get_count())
    if (users.get_count() < 10):
        while x < n:
            x += 1
            user = None
            user = UserModel()
            new_user = generate_user()
            save_data = user.clean_insert_dict(new_user,  full=False)
            save_data['password'] = hash_password(new_user['password'])
            user.insert(save_data)


def generate_user():
    return {
        "email": "email{}@mail.com".format(random_name(6)),
        "password": "password",
        "firstname": "Name",
        "othername": random_name(9),
        "lastname": random_name(15),
        "phonenumber": "089329296692",
        "passporturlstring": "www.url.com/"+random_name(9)


    }


def random_name(stringLength=10):
    """Generate a random string with
    the combination of lowercase and uppercase letters
        """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

"""
app/__init__.py
"""

import os
from flask import Flask
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
    db.create_tables()
    create_default_admin()
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

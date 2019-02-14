"""
app/__init__.py
"""


from flask import Flask, make_response, jsonify
from instance.config import configs
from app.v1 import v1_app
from app.v2 import v2_app
from app.db_setup import  DbSetup


#  polApp = create_app()


def create_app(config='development'):

    app = Flask(__name__)

    app.config.from_object(configs[config])

    app.register_blueprint(v1_app, url_prefix='/api/v1')
    app.register_blueprint(v2_app, url_prefix='/api/v2')

  
    db = DbSetup(config)
    db.create_tables()
    # db.drop()
    return app

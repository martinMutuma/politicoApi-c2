"""
app/__init__.py
"""


from flask import Flask, make_response, jsonify
from instance.config import configs
from app.v1 import v1_app
from app.db_setup import  DbSetup

# polApp = create_app()


def create_app(config='development'):

    app = Flask(__name__)

    app.config.from_object(configs[config])

    app.register_blueprint(v1_app, url_prefix='/api/v1')


    db = DbSetup(config)
    db.create_tables()
    db.drop()

 

    @app.route('/', methods=['GET'])
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

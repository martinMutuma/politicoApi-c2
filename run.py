"""run.py the main file to run the app"""

from app import create_app
from flask import make_response, jsonify
from dotenv import load_dotenv
from flasgger import Swagger

load_dotenv()
polApp = create_app('development')

polApp.config['SWAGGER'] = {
    'specs_route': '/',
}
Swagger(polApp, template_file='../api_docs.yaml')


@polApp.route('/routes', methods=['GET'])
def home():
    """Default Home route when you load the app"""
    routes = []
    for route in polApp.url_map.iter_rules():
        routes.append(str(route))
    res = dict(
        endpoints=routes,
        message="Welcome to Polical by Martin",
        status=200,
    )
    return make_response(jsonify(res), 200)


@polApp.errorhandler(404)
def endpoint_not_found(*args):
    """Handles all error 404 responses
        For compliance with API endpoint standard replies n]
    """

    res = dict(
        error="Endpoint not found",
        status=404
    )
    return make_response(jsonify(res), 404)


@polApp.errorhandler(500)
def endpoint_server_error(*args):
    """ Handles server errors
    """

    res = {
        "error": "Its not you, its us",
        "status": 500
    }
    return make_response(jsonify(res), 500)


@polApp.errorhandler(405)
def method_not_allowed(*args):
    """
    Handles method not allowed erros

    """

    res = jsonify(dict(
        error="Method not allowed",
        status=405
    ))
    return make_response(res, 405)


if __name__ == "__main__":
    polApp.run()

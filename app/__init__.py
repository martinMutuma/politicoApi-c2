"""
app/__init__.py
"""


from flask import Flask, make_response, jsonify
from instance.config import configs
from app.v1 import v1_app

polApp = Flask(__name__)

polApp.config.from_object(configs['production'])
polApp.register_blueprint(v1_app, url_prefix='/api/v1')

@polApp.route('/', methods=['GET'])
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
    res = dict(
        error = "Endpoint not found",
        status = 404
    )
    return make_response(jsonify(res), 404)


@polApp.errorhandler(500)
def endpoint_server_error(*args):
    res = dict(
        error = "Its not you, its us",
        status = 500
    )
    return make_response(jsonify(res), 500)


@polApp.errorhandler(405)
def method_not_allowed(*args):
    res = dict(
        error = "Method not allowed",
        status = 405
    )
    return make_response(jsonify(res), 405)
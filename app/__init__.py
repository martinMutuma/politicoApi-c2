from flask import Flask, make_response, jsonify
from instance.config import configs
from app.v1 import v1_app

polApp = Flask(__name__)

polApp.config.from_object(configs['production'])
polApp.register_blueprint(v1_app, url_prefix='/api/v1')

# from app.v1.views.parties import *
@polApp.route('/', methods=['GET'])
def home():
    """Default Home route when you load the app"""
    routes = []
    for route in polApp.url_map.iter_rules():
        routes.append(str(route))
    res = dict(
        data=routes,
        status=200,
    )
    return make_response(jsonify(res), 200)
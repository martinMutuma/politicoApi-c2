"""app/routes.py """

from app import polApp

from flask import url_for, jsonify, make_response

from app.v1.routes import *

@polApp.route('/', methods=['GET'])
def home():
        
    routes = []
    for route in polApp.url_map.iter_rules():
        routes.append(str(route))
    res = dict(
        data = routes,
        status =200,
    )
    return make_response(jsonify(res), 200)




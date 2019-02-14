
from flask import request, make_response, jsonify, abort
from app.v2.models.user_model import UserModel
from app.v2.views import Views
from app.v2.views.validate import Validate
from instance.config import Config
import jwt
from functools import wraps


def require_auth(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        request.user = None

        token = request.headers.get('authorization', None)

        if token:
            if token.startswith('Bearer '):
                token = token.replace('Bearer ', '')
            secret = Config.SECRET_KEY
            algo = Config.JWT_ALGORITHM
            try:
                payload = jwt.decode(token, secret, algo)
                request.user = payload['id']
                return func(*args, **kwargs)
            except (jwt.DecodeError):
                pass
        abort(make_response(jsonify({"status": 400,
                                     'error': "Invalid Token Error,Your request could not be Authenticated"}), 400))

    return func_wrapper

    """Handles user signup and login
    """


def login():
    """Will handle User login"""
    data = Views.get_data()
    Views.check_for_required_fields(
        fields=['email', 'password'], dataDict=data)

    # do validation here
    payload = {'email': data['email'], 'id': 2323, 'isadmin': True}
    token = jwt_encode(payload)
    res = {'data': {'token': token.decode(), 'user': payload
                    },
           'status': 200}
    return make_response(jsonify(res), res['status'])


def jwt_encode(payload):
    """For creating Jwt Tokens

    Arguments:
        payload {[dict]} -- [key:value]

    """

    secret = Config.SECRET_KEY
    algo = Config.JWT_ALGORITHM
    token = jwt.encode(payload, secret, algo)
    return token


@require_auth
def test():
    return make_response(jsonify({"Mesaage": "This was validated"}), 200)

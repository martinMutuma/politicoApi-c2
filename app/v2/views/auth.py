
from flask import request, make_response, jsonify, abort
from app.v2.models.user_model import UserModel
from app.v2.views import Views
from app.v2.views.validate import Validate
from instance.config import Config
import jwt
from functools import wraps


def signup():
    """
    User signup
    """

    data = Views.get_data()
    required_data = ['email', 'password', 'firstname',
                     'othername', 'lastname', 'phonenumber', 'passporturlstring']
    Views.check_for_required_fields(
        fields=required_data, dataDict=data)
    names = ['firstname', 'othername', 'lastname']
    error_message = []
    for name in names:
        valid = Validate.validate_name(data[name])
        if valid['status'] is False:
            error_message.append(valid['message'])
    validate_mail = Validate.validate_email(data['email'])
    if not validate_mail['status']:
        error_message.append(validate_mail['message'])
    validate_pass = Validate.validate_length(data['password'], 6)
    if validate_pass['status'] == False:
        error_message.append(validate_pass['message'])
    user = None
    user = UserModel()
    user.where(dict(email=data['email']))
    if user.check_exist() == True:
        error_message.append(
            "Account with email {} exists".format(data['email']))
    user2 = UserModel()
    user2.where(dict(passporturlstring=data['passporturlstring']))
    if user2.check_exist() == True:
        error_message.append(
            "Account with passport {} exists".format(data['passporturlstring']))

    if len(error_message) > 0:
        res = jsonify({'error': ",".join(error_message), 'status': 400})
        return make_response(res, 400)

    save_data = user.clean_insert_dict(data,  full=False)

    user.insert(save_data)
    returnUserDetails = user.sub_set()
    token = ''
    if user.id is not None:
        token = jwt_encode(returnUserDetails)
    res = jsonify(
        {"status": 201, 'data': {'user': returnUserDetails, 'token': token}})
    return make_response(res, 201)


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
    return token.decode()


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


@require_auth
def test():
    return make_response(jsonify({"Mesaage": "This was validated"}), 200)

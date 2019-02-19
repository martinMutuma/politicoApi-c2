import hashlib
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
                     'othername', 'lastname',
                     'phonenumber', 'passporturlstring']
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
    if validate_pass['status'] is False:
        error_message.append(validate_pass['message'])
    user = None
    user = UserModel()
    user.where(dict(email=data['email']))
    if user.check_exist() is True:
        error_message.append(
            "Account with email {} exists".format(data['email']))
    user2 = UserModel()
    user2.where(dict(passporturlstring=data['passporturlstring']))
    if user2.check_exist() is True:
        msg = "Account with passport {} exists".format(
            data['passporturlstring'])
        error_message.append(msg)

    if len(error_message) > 0:
        res = jsonify({'error': ",".join(error_message), 'status': 400})
        return make_response(res, 400)

    save_data = user.clean_insert_dict(data,  full=False)
    save_data['password'] = hash_password(data['password'])
    print(user.insert(save_data))
    returnUserDetails = user.sub_set()
    token = ''

    if user.id is not None:
        token = jwt_encode(returnUserDetails)
        data = {'user': returnUserDetails, 'token': token}
        res = jsonify(
            {"status": 201, 'data': data})
        return make_response(res, 201)
    return make_response(jsonify(
        {"Error": 'Something went wrong', 'status': 500}), 500)


def login():
    """Will handle User login"""
    data = Views.get_data()
    Views.check_for_required_fields(
        fields=['email', 'password'], dataDict=data)

    user = UserModel()
    user.where(dict(email=data['email']))
    if user.check_exist() is True and user.id is not None:
        hashpassword = hash_password(data['password'])
        if user.password == hashpassword:
            payload = user.sub_set()
            token = jwt_encode(payload)
            res = {'data': {'token': token, 'user': payload
                            },
                   'status': 200}
            return make_response(jsonify(res), res['status'])
    res = {'error': "Login error, Please check your datails", 'status': 400}
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
    """Auth Wrapper for checking Jwt token in the request

    Arguments:
        func {[type]} -- The function to authenticare

    Returns:
        [error] -- [Incase token is invalid]
        returns the function for success
    """

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        request.user = None

        token = request.headers.get('authorization', None)

        if token:
            if token.startswith('Bearer'):
                token = token.replace('Bearer', '')
                token = token.strip()
            secret = Config.SECRET_KEY
            algo = Config.JWT_ALGORITHM
            try:
                payload = jwt.decode(token, secret, algo)
                request.user = payload
                return func(*args, **kwargs)
            except (jwt.DecodeError):
                pass
        abort(make_response(jsonify(
            {"status": 400,
                'error': "You are not authorized to perform that action"}),
            400))

    return func_wrapper


def require_auth_admin(func):
    """Auth Wrapper for checking Jwt token in the request for admin routes

    Arguments:
        func {[type]} -- The function to authenticare

    Returns:
        [error] -- [Incase token is invalid]
        returns the function for success
    """
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
                isadmin = payload.get('isadmin', False)
                if isadmin is True:
                    request.user = payload
                    return func(*args, **kwargs)
            except (jwt.DecodeError):
                pass
        abort(make_response(jsonify(
            {"status": 400,
                'error': "You are not authorized to perform this action"}),
            400))

    return func_wrapper


@require_auth
def test():
    return make_response(jsonify({"Mesaage": "This was validated"}), 200)


def hash_password(password):
    """simmple password hashing

    Arguments:
        password {[str]} -- [the string to Hash]

    Returns:
        [str] -- [the hashed password]
    """

    hash_object = hashlib.md5(password.encode())
    return hash_object.hexdigest()


@require_auth_admin
def make_admin(user_id):
    data = dict(isadmin=True)
    user = UserModel()
    user.where(dict(id=user_id))
    if user.check_exist() is True and user.id is not None:
        update_data = user.clean_insert_dict(data, False)
        user.update(update_data, user_id)
        res = {"status": 202, "data": user.sub_set()}
    else:
        msg = "User not found"
        res = {"status": 404, 'error': msg}
    return make_response(jsonify(res), res['status'])

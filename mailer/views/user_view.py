from flask import Blueprint, jsonify, request
from mailer.middlewares.auth_middleware import Middlewares
from mailer.controllers.user_controller import UserController

bp = Blueprint('user', __name__)

@bp.before_request
def before_request():
    return Middlewares.authenticate_middleware()

@bp.route('/get', methods=['GET'])
def get_user():
    return UserController.get_user()

@bp.route('/update', methods=['POST'])
def update_user():
    data = request.get_json()
    return UserController.update_user(data)

@bp.route('/password', methods=['POST'])
def update_password():
    data = request.get_json()
    return UserController.update_password(data)

@bp.route('/delete', methods=['POST'])
def delete_user():
    data = request.get_json()
    return UserController.delete_user(data)

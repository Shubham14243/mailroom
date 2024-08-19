from flask import Blueprint, jsonify, request
from mailer.controllers.user_controller import UserController

bp = Blueprint('user', __name__)

@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return UserController.get_user(user_id)

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

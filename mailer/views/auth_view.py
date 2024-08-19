from flask import Blueprint, jsonify, request
from mailer.controllers.auth_controller import AuthController

bp = Blueprint('auth', __name__)

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    return AuthController.signup(data)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return AuthController.login(data)

@bp.route('/logout', methods=['POST'])
def logout():
    return AuthController.logout()

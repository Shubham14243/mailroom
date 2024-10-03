from flask import Blueprint, jsonify, request
from mailer.controllers.auth_controller import AuthController

bp = Blueprint('auth', __name__)

@bp.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    return AuthController.generate(data)

@bp.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()
    return AuthController.validate(data)

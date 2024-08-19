from flask import Blueprint, jsonify, request
from mailer.controllers.app_controller import AppController

bp = Blueprint('app', __name__)

@bp.route('/create', methods=['POST'])
def create_app():
    data = request.get_json()
    return AppController.create_app(data)

@bp.route('/getall', methods=['GET'])
def get_all():
    return AppController.get_all()

@bp.route('/<int:app_id>', methods=['GET'])
def get_app(app_id):
    return AppController.get_app(app_id)

@bp.route('/regenerate/<int:app_id>', methods=['GET'])
def regenerate_key(app_id):
    return AppController.regenerate_key(app_id)

@bp.route('/delete', methods=['POST'])
def delete_app():
    data = request.get_json()
    return AppController.delete_app(data)

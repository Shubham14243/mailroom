from flask import Blueprint, jsonify, request
from mailer.middlewares.auth_middleware import Middlewares
from mailer.controllers.templates_controller import TemplatesController

bp = Blueprint('template', __name__)

@bp.before_request
def before_request():
    return Middlewares.authenticate_middleware()

@bp.route('/<int:template_id>', methods=['GET'])
def get_template(template_id):
    return TemplatesController.get_template(template_id)

@bp.route('/getall/<int:app_id>', methods=['GET'])
def get_all(app_id):
    return TemplatesController.get_all(app_id)

@bp.route('/create', methods=['POST'])
def create_template():
    data = request.get_json()
    return TemplatesController.create_template(data)

@bp.route('/update', methods=['POST'])
def update_template():
    data = request.get_json()
    return TemplatesController.update_template(data)

@bp.route('/delete', methods=['POST'])
def delete_template():
    data = request.get_json()
    return TemplatesController.delete_template(data)

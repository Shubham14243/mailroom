from flask import Blueprint, jsonify, request
from mailer.middlewares.auth_middleware import Middlewares
from mailer.controllers.mail_controller import MailController

bp = Blueprint('mail', __name__)

@bp.before_request
def before_request():
    return Middlewares.authenticate_middleware()

@bp.route('/simple', methods=['POST'])
def simple_mail():
    data = request.get_json()
    return MailController.simple_mail(data)

@bp.route('/send', methods=['POST'])
def send_mail():
    data = request.get_json()
    return MailController.send_mail(data)

@bp.route('/logs/clear', methods=['POST'])
def clear_logs():
    data = request.get_json()
    return MailController.clear_logs(data)

@bp.route('/logs/<int:template_id>', methods=['GET'])
def get_template_logs(template_id):
    return MailController.get_template_logs(template_id)

@bp.route('/applogs/<int:app_id>', methods=['GET'])
def get_app_logs(app_id):
    return MailController.get_app_logs(app_id)

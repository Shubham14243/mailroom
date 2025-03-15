from flask import Blueprint, jsonify, request
from mailer.middlewares.auth_middleware import Middlewares
from mailer.controllers.mail_controller import MailController

bp = Blueprint('mail', __name__)

@bp.before_request
def before_request():
    skip_auth_path = ["/api/mail/simple", "/api/mail/send"]
    if request.path not in skip_auth_path:
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

@bp.route('/logs', methods=['GET'])
def get_logs():
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', type=int)
    return MailController.get_logs(limit=limit, offset=offset)

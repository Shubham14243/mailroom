from flask import Blueprint, jsonify, request
from mailer.controllers.mail_controller import MailController

bp = Blueprint('mail', __name__)

@bp.route('/simple', methods=['POST'])
def simple_mail():
    data = request.get_json()
    return MailController.simple_mail(data)

@bp.route('/send', methods=['POST'])
def send_mail():
    data = request.get_json()
    return MailController.send_mail(data)

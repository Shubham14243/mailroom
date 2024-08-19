from flask import Blueprint, jsonify, request
from mailer.controllers.mail_controller import MailController

bp = Blueprint('mail', __name__)

@bp.route('/send', methods=['POST'])
def send_mail():
    data = request.get_json()
    return MailController.send_mail(data)

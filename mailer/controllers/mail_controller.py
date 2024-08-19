from flask import jsonify, make_response, request
from mailer import db
from mailer import mail
from flask_mail import Message
import datetime
from mailer.models.templates import Templates
from mailer.util.validator import Validator
from mailer.util.user_token import UserToken
from mailer.config.config import Config
from mailer.util.mail import Mail

class MailController:
        
    @staticmethod
    def send_mail(data):
        
        try:
            
            payload = UserToken.verify_token()
            
            if payload['user_id'] == 'exp':
                response = {
                    "code": 401,
                    "status": "failure",
                    "message": "Token Expired"
                }
                return jsonify(response), 401
            elif payload['user_id'] == 'inv':
                response = {
                    "code": 401,
                    "status": "failure",
                    "message": "Invalid Token!"
                }
                return jsonify(response), 401
            
            user_id = payload['user_id']
            
            if isinstance(user_id, str):
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid UserID!"
                }
                return jsonify(response), 400
            
            if Validator.validate_email(data['recipient']) == False:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Recipient!"
                }
                return jsonify(response), 400
            
            template = Templates.query.filter_by(template_id=data['template_id']).first()
            
            if not template:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Template!"
                }
                return jsonify(response), 400
            
            mail_body = template.body
            
            for key, value in data['params'].items():
                mail_body = mail_body.replace(f"{{{{{key}}}}}", str(value))
            
            msg = Message(
                subject=template.subject,
                sender=template.sender_email,
                recipients=[data['recipient']],
                body=mail_body
            )
            
            mail.send(msg)
            
            response = {
                "code": 200,
                "status": "success",
                "message": "Email Sent Successfully!"
            }
            response['recipient'] = data['recipient']
            response['subject'] = template.subject
            
            return jsonify(response), 200
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error Mail Send Controller! {e}"
            }
            return jsonify(response), 500
        
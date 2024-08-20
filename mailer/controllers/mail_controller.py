from flask import jsonify, make_response, request
from mailer import db
from mailer import mail
from flask_mail import Message
import datetime
import json
from mailer.models.templates import Templates
from mailer.models.mail_log import MailLog
from mailer.models.app import App
from mailer.util.validator import Validator
from mailer.util.user_token import UserToken
from mailer.config.config import Config

class MailController:
    
    @staticmethod
    def simple_mail(data):
        
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
            
            if Validator.validate_email(data['recipient']) == False or Validator.validate_subject(data['subject']) == False or Validator.validate_subject(data['sender_name']) == False:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Data!"
                }
                return jsonify(response), 400
            
            msg = Message(
                subject=data['subject'],
                sender=(data['sender_name'], data['sender']),
                recipients=[data['recipient']],
                body=data['body']
            )
            
            mail.send(msg)
            
            app = App.query.filter_by(user_id=user_id).first()
            
            app_id = app.app_id if app else 0
            
            new_log = MailLog(
                app_id = app_id,
                template_id = 0,
                to_email = data['recipient'],
                from_email = data['sender'],
                subject = data['subject'],
                status = "success",
                sent_at = datetime.datetime.utcnow()
            )
            
            db.session.add(new_log)
            db.session.commit()
            
            response = {
                "code": 200,
                "status": "success",
                "message": "Email Sent Successfully!"
            }
            response['recipient'] = data['recipient']
            response['subject'] = data['subject']
            
            return jsonify(response), 200
        
        except Exception as e:
            
            new_log = MailLog(
                app_id = app_id,
                template_id = 0,
                to_email = data['recipient'],
                from_email = data['sender'],
                subject = data['subject'],
                status = "failure",
                sent_at = datetime.datetime.utcnow()
            )
            
            db.session.add(new_log)
            db.session.commit()
            
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error Mail Send Controller! {e}"
            }
            return jsonify(response), 500
        
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
                
            if template.is_html == False:
                msg = Message(
                    subject=template.subject,
                    sender=(template.sender_name, template.sender_email),
                    recipients=[data['recipient']],
                    body=mail_body
                )
                
                mail.send(msg)
            else:
                msg = Message(
                    subject=template.subject,
                    sender=(template.sender_name, template.sender_email),
                    recipients=[data['recipient']],
                    html=mail_body
                )
                
                mail.send(msg)
            
            new_log = MailLog(
                app_id = template.app_id,
                template_id = template.template_id,
                to_email = data['recipient'],
                from_email = template.sender_email,
                subject = template.subject,
                body_data = json.dumps(data['params']),
                status = "success",
                sent_at = datetime.datetime.utcnow()
            )
            
            db.session.add(new_log)
            db.session.commit()
            
            response = {
                "code": 200,
                "status": "success",
                "message": "Email Sent Successfully!"
            }
            response['recipient'] = data['recipient']
            response['subject'] = template.subject
            
            return jsonify(response), 200
        
        except Exception as e:
            
            new_log = MailLog(
                app_id = template.app_id,
                template_id = template.template_id,
                to_email = data['recipient'],
                from_email = template.sender_email,
                subject = template.subject,
                body_data = json.dumps(data['params']),
                status = "failure",
                sent_at = datetime.datetime.utcnow()
            )
            
            db.session.add(new_log)
            db.session.commit()
            
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error Mail Send Controller! {e}"
            }
            return jsonify(response), 500
        
    @staticmethod
    def get_template_logs(template_id):
        
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
            
            logs = MailLog.query.filter_by(template_id=template_id).all()
            
            if not logs:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Template or No Logs!"
                }
                return jsonify(response), 400
            
            response = {
                "code": 200,
                "status": "success",
                "message": "Template Logs Found Successfully!"
            }
            response['logs'] = [log.to_dict() for log in logs]
            
            return jsonify(response), 200
        
        except Exception as e:
            
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error Mail Template Logs Controller! {e}"
            }
            return jsonify(response), 500
        
    @staticmethod
    def get_app_logs(app_id):
        
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
            
            logs = MailLog.query.filter_by(app_id=app_id).all()
            
            if not logs:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid App or No Logs!"
                }
                return jsonify(response), 400
            
            response = {
                "code": 200,
                "status": "success",
                "message": "App Logs Found Successfully!"
            }
            response['logs'] = [log.to_dict() for log in logs]
            
            return jsonify(response), 200
        
        except Exception as e:
            
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error Mail App Logs Controller! {e}"
            }
            return jsonify(response), 500
    
    @staticmethod
    def clear_logs(data):
    
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
            
            logs = MailLog.query.filter_by(template_id=data['template_id']).all()
            
            if not logs:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Template Logs does not Exists!"
                }
                return jsonify(response), 400
            
            for log in logs:
                db.session.delete(log)
                db.session.commit()
            
            response = make_response(
                    jsonify({
                    "code": 200,
                    "status": "success",
                    "message": "Template Logs Cleared Successfully!"
                }), 200
            )
            
            return response
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error Mail Logs Clear Controller! {e}"
            }
            return jsonify(response), 500
        
    
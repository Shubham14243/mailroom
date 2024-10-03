from flask import jsonify, make_response, request, g
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
from mailer.util.api_key import ApiKey

class MailController:
    
    @staticmethod
    def simple_mail(data):
        
        try:
            
            req_params = ['mailkey', 'app_id', 'sender', 'sender_name', 'recipient', 'subject', 'body']
            
            for par in req_params:
                if par not in data.keys():
                    response = {
                        "code": 400,
                        "status": "failure",
                        "message": "Incomplete Request Body!"
                    }
                    return jsonify(response), 400
            
            user_id = g.user
            mailkey = data['mailkey']
            app_id = data['app_id']
            sender = data['sender']
            sender_name = data['sender_name']
            recipient = data['recipient']
            subject = data['subject']
            body = data['body']
            
            check_flag = 1
            error_str = 'Invalid Data!'
            error_val = None
                
            error_val =  Validator.validate_email(sender)
            
            if error_val != None:
                error_str += error_val
                check_flag = 0
                
            error_val =  Validator.validate_name(sender_name)
            
            if error_val != None:
                error_str += error_val
                check_flag = 0
                
            error_val =  Validator.validate_email(recipient)
            
            if error_val != None:
                error_str += error_val
                check_flag = 0
                
            error_val =  Validator.validate_subject(subject)
            
            if error_val != None:
                error_str += error_val
                check_flag = 0
            
            if check_flag == 0:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": error_str
                }
                return jsonify(response), 400
            
            app = App.query.filter_by(app_id=app_id, user_id=user_id).first()
            if not app:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "App does not Exists!"
                }
                return jsonify(response), 400
            
            api_user = api_app = ''
            api_user, api_app = ApiKey.verify_api_key(mailkey)
            
            if api_app != int(app_id) or api_user != user_id:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Email Mail Key!"
                }
                return jsonify(response), 400
            
            msg = Message(
                subject=subject,
                sender=(sender_name, sender),
                recipients=[recipient],
                body=body
            )
            
            mail.send(msg)
            
            new_log = MailLog(
                app_id = app_id,
                template_id = 0,
                to_email = recipient,
                from_email = sender,
                subject = subject,
                body_data = json.dumps({}),
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
            response['recipient'] = recipient
            response['subject'] = subject
            
            return jsonify(response), 200
        
        except Exception as e:
            
            new_log = MailLog(
                app_id = app_id,
                template_id = 0,
                to_email = recipient,
                from_email = sender,
                subject = subject,
                body_data = json.dumps({}),
                status = "failure",
                sent_at = datetime.datetime.utcnow()
            )
            
            db.session.add(new_log)
            db.session.commit()
            
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error Mail Simple Controller! {e}"
            }
            return jsonify(response), 500
        
    @staticmethod
    def send_mail(data):
        
        try:
            
            req_params = ['mailkey', 'recipient', 'params', 'template_id']
            
            for par in req_params:
                if par not in data.keys():
                    response = {
                        "code": 400,
                        "status": "failure",
                        "message": "Incomplete Request Body!"
                    }
                    return jsonify(response), 400
            
            user_id = g.user
            mailkey = data['mailkey']
            recipient = data['recipient']
            params = data['params']
            template_id = data['template_id']
            
            for emails in data['recipient']:
                if Validator.validate_email(emails) != None:
                    response = {
                        "code": 400,
                        "status": "failure",
                        "message": "Invalid Recipient!"
                    }
                    return jsonify(response), 400
            
            template = Templates.query.filter_by(template_id=template_id).first()
            
            if not template:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Template does not Exists!"
                }
                return jsonify(response), 400
            
            app_id = int(template.app_id)
            
            app_data = App.query.filter_by(app_id=app_id, user_id=user_id).first()
            if not app_data:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Template!"
                }
                return jsonify(response), 400
            
            api_user = api_app = ''
            api_user, api_app = ApiKey.verify_api_key(mailkey)
            
            if api_app != app_id or api_user != user_id:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Email Mail Key!"
                }
                return jsonify(response), 400
            
            mail_body = template.body
            
            for key, value in params.items():
                mail_body = mail_body.replace(f"{{{{{key}}}}}", str(value))
                
            if template.is_html == False:
                msg = Message(
                    subject=template.subject,
                    sender=(template.sender_name, template.sender_email),
                    recipients=recipient,
                    body=mail_body
                )
                
                mail.send(msg)
            else:
                msg = Message(
                    subject=template.subject,
                    sender=(template.sender_name, template.sender_email),
                    recipients=recipient,
                    html=mail_body
                )
                
                mail.send(msg)
                
            email_list = ''
                
            for emails in recipient:
                email_list += emails
                email_list += '/'
            
            new_log = MailLog(
                app_id = template.app_id,
                template_id = template.template_id,
                to_email = email_list,
                from_email = template.sender_email,
                subject = template.subject,
                body_data = json.dumps(params),
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
            response['recipient'] = recipient
            response['subject'] = template.subject
            
            return jsonify(response), 200
        
        except Exception as e:
            
            new_log = MailLog(
                app_id = template.app_id,
                template_id = template.template_id,
                to_email = recipient,
                from_email = template.sender_email,
                subject = template.subject,
                body_data = json.dumps(params),
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
            
            user_id = g.user
            
            template = Templates.query.filter_by(template_id=template_id).first()
            
            if not template:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Template does not Exists!"
                }
                return jsonify(response), 400
            
            app_id = int(template.app_id)
            
            app_data = App.query.filter_by(app_id=app_id, user_id=user_id).first()
            if not app_data:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Template!"
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
            
            user_id = g.user
            
            app_data = App.query.filter_by(app_id=app_id, user_id=user_id).first()
            if not app_data:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid App!"
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
            
            req_params = ['template_id']
            
            for par in req_params:
                if par not in data.keys():
                    response = {
                        "code": 400,
                        "status": "failure",
                        "message": "Incomplete Request Body!"
                    }
                    return jsonify(response), 400
            
            user_id = g.user
            template_id = data['template_id']
            
            template = Templates.query.filter_by(template_id=template_id).first()
            
            if not template:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Template does not Exists!"
                }
                return jsonify(response), 400
            
            app_id = int(template.app_id)
            
            app_data = App.query.filter_by(app_id=app_id, user_id=user_id).first()
            if not app_data:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Template!"
                }
                return jsonify(response), 400
            
            logs = MailLog.query.filter_by(template_id=template_id).all()
            
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
        
    
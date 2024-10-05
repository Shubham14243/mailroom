from flask import jsonify, make_response, request, g
from mailer import db
import datetime
from mailer.models.templates import Templates
from mailer.models.app import App
from mailer.models.user import User
from mailer.models.mail_log import MailLog
from mailer.util.encryptor import Encryptor
from mailer.util.validator import Validator
from mailer.util.html_parser import HTMLParser

class TemplatesController:
    
    @staticmethod
    def validate_template(template_id, user_id):
        
        user_data = User.query.filter_by(id=user_id).first()
        if not user_data:
            return None

        app_data = App.query.filter_by(user_id=user_id).all()
        if not app_data or app_data == []:
            return None
        
        apps = []
        
        for app in app_data:
            apps.append(app.app_id)
        
        for app in apps:
            template = Templates.query.filter_by(app_id=app, template_id=template_id).first()
            if template:
                return template
            
        return None
    
    @staticmethod
    def get_template(template_id):
        
        try:
            
            user_id = g.user
            
            template = TemplatesController.validate_template(template_id, user_id)
            
            if not template:
                response = {
                    "code": 404,
                    "status": "failure",
                    "message": "Template not Found!"
                }
                return jsonify(response), 404
            
            response = {
                "code": 200,
                "status": "success",
                "message": "Template Found Successfully!"
            }
            response['template'] = template.to_dict()
            
            return jsonify(response), 200
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error Template Get Controller! {e}"
            }
            return jsonify(response), 500
        
    
    @staticmethod
    def get_all(app_id):
        
        try:
            
            user_id = g.user
            
            app_data = App.query.filter_by(user_id=user_id, app_id=app_id).first()
            
            if not app_data:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid App!"
                }
                return jsonify(response), 400
            
            templates_data = Templates.query.filter_by(app_id=app_id).all()
            
            if not templates_data:
                response = {
                    "code": 404,
                    "status": "failure",
                    "message": "App Templates Not Found!"
                }
                return jsonify(response), 404
            
            response = {
                "code": 200,
                "status": "success",
                "message": "App Templates Found Successfully!"
            }
            response['templates'] = [template.to_dict() for template in templates_data]
            
            return jsonify(response), 200
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error Template GetAll Controller! {e}"
            }
            return jsonify(response), 500
    
    @staticmethod
    def create_template(data):
        
        try:
            
            req_params = ['app_id', 'name', 'subject', 'sender_name', 'sender_email', 'body', 'is_html']
            
            for par in req_params:
                if par not in data.keys():
                    response = {
                        "code": 400,
                        "status": "failure",
                        "message": "Incomplete Request Body!"
                    }
                    return jsonify(response), 400
            
            user_id = g.user
            app_id = data['app_id']
            name = data['name']
            subject = data['subject']
            sender_name = data['sender_name']
            sender_email = data['sender_email']
            body = data['body']
            is_html = data['is_html']
            
            check_flag = 1
            error_str = 'Invalid Data!'
            error_val = None
                
            error_val =  Validator.validate_name(name)
            
            if error_val != None:
                error_str += error_val
                check_flag = 0
                
            error_val =  Validator.validate_name(sender_name)
            
            if error_val != None:
                error_str += error_val
                check_flag = 0
                
            error_val =  Validator.validate_subject(subject)
            
            if error_val != None:
                error_str += error_val
                check_flag = 0
                
            error_val =  Validator.validate_email(sender_email)
            
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
            
            if (is_html == False and HTMLParser.is_valid_text(body) == False) or (is_html == True and HTMLParser.is_valid_html(body) == False):
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Data! Invalid Body!"
                }
                return jsonify(response), 400
            
            app_data = App.query.filter_by(app_id=app_id, user_id=user_id).first()
            
            if not app_data:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "App does not Exists!"
                }
                return jsonify(response), 400
                
            new_template = Templates(
                app_id = data['app_id'],
                name = data['name'],
                subject = data['subject'],
                sender_name = data['sender_name'],
                sender_email = data['sender_email'],
                body = data['body'],
                is_html = data['is_html'],
                created_at=datetime.datetime.utcnow()
            )
            
            db.session.add(new_template)
            db.session.commit()
            
            response = {
                "code": 201,
                "status": "success",
                "message": "Template Created Successfully!",
                "template": new_template.to_dict()
            }
            
            return jsonify(response), 201
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error Template Create Controller! {e}"
            }
            return jsonify(response), 500
    
    @staticmethod
    def update_template(data):
        
        try:
            
            req_params = ['template_id', 'name', 'subject', 'sender_name', 'sender_email', 'body', 'is_html']
            
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
            name = data['name']
            subject = data['subject']
            sender_name = data['sender_name']
            sender_email = data['sender_email']
            body = data['body']
            is_html = data['is_html']
            
            check_flag = 1
            error_str = 'Invalid Data!'
            error_val = None
                
            error_val =  Validator.validate_name(name)
            
            if error_val != None:
                error_str += error_val
                check_flag = 0
                
            error_val =  Validator.validate_name(sender_name)
            
            if error_val != None:
                error_str += error_val
                check_flag = 0
                
            error_val =  Validator.validate_subject(subject)
            
            if error_val != None:
                error_str += error_val
                check_flag = 0
                
            error_val =  Validator.validate_email(sender_email)
            
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
            
            if (is_html == False and HTMLParser.is_valid_text(body) == False) or (is_html == True and HTMLParser.is_valid_html(body) == False):
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Body!"
                }
                return jsonify(response), 400
            
            template = TemplatesController.validate_template(template_id, user_id)
            
            if not template:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Template does not Exists!"
                }
                return jsonify(response), 400
                
            template.name = name  if name else template.name
            template.subject = subject if subject else template.subject
            template.sender_name = sender_name if sender_name else template.sender_name
            template.sender_email = sender_email if sender_email else template.sender_email
            template.body = body if body else template.body
            template.is_html = is_html if is_html is not None else template.is_html
            db.session.commit()
            
            response = {
                "code": 200,
                "status": "success",
                "message": "Template Updated Successfully!",
                "template": template.to_dict()
            }
            
            return jsonify(response), 200
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error Template Update Controller! {e}"
            }
            return jsonify(response), 500
    
    @staticmethod
    def delete_template(data):
    
        try:
            
            req_params = ['template_id', 'password']
            
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
            password = data['password']
            
            if Validator.validate_password(password) != None:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Data! Invalid Password!"
                }
                return jsonify(response), 400
            
            template = TemplatesController.validate_template(template_id, user_id)
            
            if not template:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Template does not Exists!"
                }
                return jsonify(response), 400
            
            existing_user = User.query.filter_by(id=user_id).first()
            if not existing_user:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "User does not Exists!"
                }
                return jsonify(response), 400
            
            password_hash = existing_user.get_password_hash()
            
            if not Encryptor.verify_password(password_hash, password) :
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Password!"
                }
                return jsonify(response), 400
            
            logs = MailLog.query.filter_by(template_id=template_id).all()
            for log in logs:
                db.session.delete(log)
            
            db.session.delete(template)
            db.session.commit()
            
            response = {
                    "code": 200,
                    "status": "success",
                    "message": "Template Deleted Successfully!"
                }
            
            return jsonify(response), 200
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error Template Delete Controller! {e}"
            }
            return jsonify(response), 500
        
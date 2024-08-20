from flask import jsonify, make_response, request
from mailer import db
import datetime
from mailer.models.templates import Templates
from mailer.util.validator import Validator
from mailer.util.user_token import UserToken
from mailer.util.html_parser import HTMLParser

class TemplatesController:
    
    @staticmethod
    def get_template(template_id):
        
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
            
            template = Templates.query.filter_by(template_id=template_id).first()
            
            if not template:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Template does not Exists!"
                }
                return jsonify(response), 400
            
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
            
            if isinstance(payload['user_id'], str):
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid UserID!"
                }
                return jsonify(response), 400
            
            if Validator.validate_name(data['name']) == False or Validator.validate_name(data['sender_name']) == False or Validator.validate_subject(data['subject']) == False or Validator.validate_name(data['sender_email']) == False:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Data!"
                }
                return jsonify(response), 400
            
            if HTMLParser.text_body(data['body']) == False:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Body!"
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
                "message": "App Created Successfully!",
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
            
            if isinstance(payload['user_id'], str):
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid UserID!"
                }
                return jsonify(response), 400
            
            if Validator.validate_name(data['name']) == False or Validator.validate_name(data['sender_name']) == False or Validator.validate_subject(data['subject']) == False or Validator.validate_name(data['sender_email']) == False:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Data!"
                }
                return jsonify(response), 400
            
            if HTMLParser.text_body(data['body']) == False:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Body!"
                }
                return jsonify(response), 400
            
            template = Templates.query.filter_by(template_id=data['template_id']).first()
            
            if not template:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Template does not Exists!"
                }
                return jsonify(response), 400
                
            template.name = data.get('name', template.name)
            template.subject = data.get('subject', template.subject)
            template.sender_name = data.get('sender_name', template.sender_name)
            template.sender_email = data.get('sender_email', template.sender_email)
            template.body = data.get('body', template.body)
            template.is_html = data.get('is_html', template.is_html)
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
            
            template = Templates.query.filter_by(template_id=data['template_id']).first()
            
            if not template:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Template does not Exists!"
                }
                return jsonify(response), 400
            
            db.session.delete(template)
            db.session.commit()
            
            response = make_response(
                    jsonify({
                    "code": 200,
                    "status": "success",
                    "message": "Template Deleted Successfully!"
                }), 200
            )
            
            return response
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error Template Delete Controller! {e}"
            }
            return jsonify(response), 500
        
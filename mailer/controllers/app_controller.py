from flask import jsonify, make_response, request, g
from mailer import db
import datetime
from mailer.models.app import App
from mailer.models.user import User
from mailer.models.templates import Templates
from mailer.models.mail_log import MailLog
from mailer.util.validator import Validator
from mailer.util.api_key import ApiKey
from mailer.util.encryptor import Encryptor

class AppController:
    
    @staticmethod
    def regenerate_api_key(app_id, user_id):
        try:
            
            data = {
                'api_key':  ApiKey.generate_api_key(user_id, app_id),
                'created_at': datetime.datetime.utcnow()
            }
            
            user_app = App.query.filter_by(app_id=app_id).first()
            
            user_app.api_key = data.get('api_key', user_app.api_key)
            user_app.created_at = data.get('created_at', user_app.created_at)
            
            db.session.commit()
            
            return True
        
        except:
            
            return False
        
    
    @staticmethod
    def regenerate_key(app_id):
        
        try:
            
            user_id = g.user
            user_app = App.query.filter_by(app_id=app_id, user_id=user_id).first()
            
            if not user_app:
                response = {
                    "code": 404,
                    "status": "failure",
                    "message": "User App Not Found!"
                }
                return jsonify(response), 404
            
            AppController.regenerate_api_key(app_id, user_id)
            
            user_app = App.query.filter_by(app_id=app_id).first()
            
            response = {
                "code": 200,
                "status": "success",
                "message": "Api Key Regenerated Successfully!",
                "app": user_app.to_dict()
            }
            
            return jsonify(response), 200
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error App Regenerate Controller! {e}"
            }
            return jsonify(response), 500
        
    
    @staticmethod
    def get_all():
        
        try:
            
            user_id = g.user
            
            user_app = App.query.filter_by(user_id=user_id).all()
            
            if not user_app:
                response = {
                    "code": 404,
                    "status": "failure",
                    "message": "User Apps Not Found!"
                }
                return jsonify(response), 404
            
            response = {
                "code": 200,
                "status": "success",
                "message": "User Apps Found Successfully!"
            }
            response['apps'] = [apps.to_dict() for apps in user_app]
            
            return jsonify(response), 200
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error App GetAll Controller! {e}"
            }
            return jsonify(response), 500
        
    
    @staticmethod
    def get_app(app_id):
        
        try:
            
            user_id = g.user
            
            user_app = App.query.filter_by(app_id=app_id, user_id=user_id).first()
            
            if not user_app:
                response = {
                    "code": 404,
                    "status": "failure",
                    "message": "User App Not Found!"
                }
                return jsonify(response), 404
            
            response = {
                "code": 200,
                "status": "success",
                "message": "App Found Successfully!"
            }
            response['app'] = user_app.to_dict()
            
            return jsonify(response), 200
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error App Get Controller! {e}"
            }
            return jsonify(response), 500
            
    
    @staticmethod
    def create_app(data):
        
        try:
            
            req_params = ['app_name']
            
            for par in req_params:
                if par not in data.keys():
                    response = {
                        "code": 400,
                        "status": "failure",
                        "message": "Incomplete Request Body!"
                    }
                    return jsonify(response), 400
            
            user_id = g.user
            app_name = data['app_name']
            
            check_flag = 1
            error_str = 'Invalid Data!'
            error_val = None
                
            error_val =  Validator.validate_name(app_name)
            
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
            
            api_key = ''
            created_at = datetime.datetime.utcnow()
            
            new_app = App(
                user_id=user_id,
                app_name=app_name,
                api_key=api_key,
                created_at=created_at
            )
            
            db.session.add(new_app)
            db.session.commit()
            
            app_id = new_app.app_id
            
            AppController.regenerate_api_key(app_id, user_id)
            
            user_app = App.query.filter_by(app_id=app_id).first()
            
            response = {
                "code": 201,
                "status": "success",
                "message": "App Created Successfully!",
                "app": user_app.to_dict()
            }
            
            return jsonify(response), 201
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error App Create Controller! {e}"
            }
            return jsonify(response), 500
    
    @staticmethod
    def delete_app(data):
    
        try:
            
            req_params = ['app_id', 'password']
            
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
            password = data['password']
            
            if Validator.validate_password(password) != None:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Data! Invalid Password!"
                }
                return jsonify(response), 400
            
            user_app = App.query.filter_by(app_id=app_id, user_id=user_id).first()
            
            if not user_app:
                response = {
                    "code": 404,
                    "status": "failure",
                    "message": "User App not Found!"
                }
                return jsonify(response), 404
            
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
            
            logs = MailLog.query.filter_by(app_id=app_id).all()
            for log in logs:
                db.session.delete(log)
            
            templates = Templates.query.filter_by(app_id=app_id).all()
            for template in templates:
                db.session.delete(template)
            
            db.session.delete(user_app)
            db.session.commit()
            
            response = {
                "code": 200,
                "status": "success",
                "message": "App Deleted Successfully!"
            }
            
            return jsonify(response), 200
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error App Delete Controller! {e}"
            }
            return jsonify(response), 500
        
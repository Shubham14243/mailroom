from flask import jsonify, make_response, request, g
from mailer import db
from mailer.models.user import User
from mailer.models.app import App
from mailer.models.templates import Templates
from mailer.models.mail_log import MailLog
from mailer.util.validator import Validator
from mailer.util.encryptor import Encryptor

class UserController:

    @staticmethod
    def get_user():
        
        try:
            
            user_id = g.user
            
            user = User.query.filter_by(id=user_id).first()
            
            if not user:
                response = {
                    "code": 404,
                    "status": "failure",
                    "message": "User Not Found!"
                }
                return jsonify(response), 404
            
            response = {
                "code": 200,
                "status": "success",
                "message": "User Found Successfully!"
            }
            response['user'] = user.to_dict()
            
            return jsonify(response), 200
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error User Get Controller! {e}"
            }
            return jsonify(response), 500

    @staticmethod
    def update_user(data):
        
        try:
            
            req_params = ['name', 'email']
            
            for par in req_params:
                if par not in data.keys():
                    response = {
                        "code": 400,
                        "status": "failure",
                        "message": "Incomplete Request Body!"
                    }
                    return jsonify(response), 400
            
            user_id = g.user
            email = data['email']
            name = data['name']
            
            check_flag = 1
            error_str = 'Invalid Data!'
            error_val = None
                
            error_val =  Validator.validate_email(email)
            
            if error_val != None:
                error_str += error_val
                check_flag = 0
                    
            error_val =  Validator.validate_name(name)
            
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
            
            user = User.query.filter_by(id=user_id).first()
            
            if user.email != email:           
                existing_user = User.query.filter_by(email=email).first()
                if existing_user:
                    response = {
                        "code": 400,
                        "status": "failure",
                        "message": "Email already Exists!"
                    }
                    return jsonify(response), 400
            
            user.name = name if name else user.name
            user.email = email if email else user.email
            db.session.commit()
            
            response = {
                "code": 200,
                "status": "success",
                "message": "User Updated Successfully!"
            }
            return jsonify(response), 200
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error User Update Controller! {e}"
            }
            return jsonify(response), 500

    @staticmethod
    def update_password(data):
        
        try:
            
            req_params = ['current_password', 'new_password', 'confirm_password']
            
            for par in req_params:
                if par not in data.keys():
                    response = {
                        "code": 400,
                        "status": "failure",
                        "message": "Incomplete Request Body!"
                    }
                    return jsonify(response), 400
            
            user_id = g.user
            current_password = data['current_password']
            new_password = data['new_password']
            confirm_password = data['confirm_password']
        
            if new_password != confirm_password:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "New Password and Confirm Password not Matched!"
                }
                return jsonify(response), 400
            
            check_flag = 1
            error_str = 'Invalid Data!'
            error_val = None
                
            error_val =  Validator.validate_password(current_password)
            
            if error_val != None:
                error_str += 'Current Password!'
                error_str += error_val
                check_flag = 0
                
            error_val =  Validator.validate_password(new_password)
            
            if error_val != None:
                error_str += 'New Password!'
                error_str += error_val
                check_flag = 0
                
            error_val =  Validator.validate_password(confirm_password)
            
            if error_val != None:
                error_str += 'Confirm Password!'
                error_str += error_val
                check_flag = 0
            
            if check_flag == 0:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": error_str
                }
                return jsonify(response), 400
            
            user = User.query.filter_by(id=user_id).first()
            
            password_hash = user.get_password_hash()
            
            if not Encryptor.verify_password(password_hash, current_password) :
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Current Password!"
                }
                return jsonify(response), 400
            
            new_password = Encryptor.encrypt_password(data['new_password'])
            
            user.password = new_password if new_password else user.password
            db.session.commit()
            
            response = {
                "code": 200,
                "status": "success",
                "message": "Password Updated Successfully!"
            }
            return jsonify(response), 200
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error User Password Controller! {e}"
            }
            return jsonify(response), 500

    @staticmethod
    def delete_user(data):
    
        try:
            
            req_params = ['user_id', 'password']
            
            for par in req_params:
                if par not in data.keys():
                    response = {
                        "code": 400,
                        "status": "failure",
                        "message": "Incomplete Request Body!"
                    }
                    return jsonify(response), 400
            
            user_id = g.user
            req_user_id = data['user_id']
            password = data['password']
            
            if user_id != int(req_user_id):
                response = {
                        "code": 400,
                        "status": "failure",
                        "message": "Invalid User!"
                    }
                return jsonify(response), 400
            
            check_flag = 1
            error_str = 'Invalid Data!'
            error_val = None
                
            error_val =  Validator.validate_password(password)
            
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
            
            user = User.query.filter_by(id=user_id).first()
            if not user:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "User does not Exists!"
                }
                return jsonify(response), 400
            
            password_hash = user.get_password_hash()
            
            if not Encryptor.verify_password(password_hash, password) :
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid User Password!"
                }
                return jsonify(response), 400
            
            apps = App.query.filter_by(user_id=user_id).all()
            
            with db.session.no_autoflush:
                
                logs_to_delete = []
                templates_to_delete = []
                
                for app in apps:
                    logs = MailLog.query.filter_by(app_id=app.app_id).all()
                    logs_to_delete.extend(logs)
                    
                    templates = Templates.query.filter_by(app_id=app.app_id).all()
                    templates_to_delete.extend(templates)

                for log in logs_to_delete:
                    db.session.delete(log)
                for template in templates_to_delete:
                    db.session.delete(template)
                    
                for app in apps:
                    db.session.delete(app)
            
            db.session.delete(user)
            db.session.commit()
            
            response = {
                "code": 200,
                "status": "success",
                "message": "User Deleted Successfully!"
            }
            
            return jsonify(response), 200
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error User Delete Controller! {e}"
            }
            return jsonify(response), 500

from flask import jsonify, make_response
from mailer import db
from mailer.models.user import User
from mailer.util.validator import Validator
from mailer.util.encryptor import Encryptor
from mailer.config.config import Config
from mailer.middlewares.origin_check import Origin

class AdminController:

    @staticmethod
    def create(data):
        
        try:
            
            req_params = ['name', 'email', 'password', 'confirm_password', 'domain', 'creator']
            
            for par in req_params:
                if par not in data.keys():
                    response = {
                        "code": 400,
                        "status": "failure",
                        "message": "Incomplete Request Body!"
                    }
                    return jsonify(response), 400
                
            name = data['name']
            email = data['email']
            password = data['password']
            confirm_password = data['confirm_password']
            domain = data['domain']
            creator = data['creator']
            
            if creator != Config.CREATOR:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Illegal User Creation!"
                }
                return jsonify(response), 400
        
            if password != confirm_password:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Password and Confirm Password not Matched!"
                }
                return jsonify(response), 400
            
            check_flag = 1
            error_str = 'Invalid Data!'
            error_val = None
            
            error_val =  Validator.validate_domain(domain)
            
            if error_val != None:
                error_str += error_val
                check_flag = 0
            
            error_val =  Validator.validate_email(email)
            
            if error_val != None:
                error_str += error_val
                check_flag = 0
            
            error_val =  Validator.validate_name(name)
            
            if error_val != None:
                error_str += error_val
                check_flag = 0
            
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
            
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "User already Exists!"
                }
                return jsonify(response), 400
            
            password_hash = Encryptor.encrypt_password(password)
            
            new_user = User(
                name=name,
                email=email,
                password=password_hash,
                userdomain=domain
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            Origin.add_domain(new_user.id, domain)
            
            response = {}
            response['user'] = new_user.to_dict()
            response["status"] = "success"
            response["code"] = 201
            response["message"] = "User Created Successfully!"
            
            return jsonify(response), 201
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error Admin User Create Controller! {e}"
            }
            return jsonify(response), 500
        
    @staticmethod
    def update_domain(data):
        
        try:
            
            req_params = ['creator', 'domain', 'user_id']
            
            for par in req_params:
                if par not in data.keys():
                    response = {
                        "code": 400,
                        "status": "failure",
                        "message": "Incomplete Request Body!"
                    }
                    return jsonify(response), 400
                
            creator = data['creator']
            domain = data['domain']
            user_id = data['user_id']
            
            if creator != Config.CREATOR:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Illegal User Domain Updation!"
                }
                return jsonify(response), 400
            
            if Validator.validate_domain(domain) == False:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Data! Invalid Domain!"
                }
                return jsonify(response), 400
            
            existing_user = User.query.filter_by(id=user_id).first()
            if not existing_user:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "User Does Not Exists!"
                }
                return jsonify(response), 400
            
            existing_user.userdomain = domain
            db.session.commit()
            
            Origin.update_domain(existing_user.id, domain)
            
            response = {}
            response['domain'] = domain
            response["status"] = "success"
            response["code"] = 200
            response["message"] = "User Domain Updated Successfully!"
            
            return jsonify(response), 200
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error Admin User Update Domain Controller! {e}"
            }
            return jsonify(response), 500

from flask import jsonify, make_response, request
from mailer import db
import datetime
from mailer.models.user import User
from mailer.util.validator import Validator
from mailer.util.encryptor import Encryptor
from mailer.util.user_token import UserToken
from mailer.middlewares.auth_middleware import Middlewares

class AuthController:

    @staticmethod
    def generate(data):
        
        try:
            
            req_params = ['email', 'password']
            
            for par in req_params:
                if par not in data.keys():
                    response = {
                        "code": 400,
                        "status": "failure",
                        "message": "Incomplete Request Body!"
                    }
                    return jsonify(response), 400
                
            email = data['email']
            password = data['password']
            
            if Validator.validate_email(email) == False or Validator.validate_password(password) == False:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Data! Invalid Email or Password!"
                }
                return jsonify(response), 400
            
            existing_user = User.query.filter_by(email=email).first()
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
            
            new_user = existing_user.to_dict()
            
            user_id = new_user['id']
            
            cors_res = Middlewares.cors_check(user_id)
            
            if cors_res is not None:
                return cors_res
            
            token_response = UserToken.generate_token(user_id)
            
            if token_response == None:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Failed to Generate Token!"
                }
                return jsonify(response), 400
            
            user_token = token_response['token']
            token_expiry = token_response['exp']
            
            existing_user.authtoken = user_token
            db.session.commit()
            
            response = {}
            response["status"] = "success"
            response["code"] = 200
            response["token"] = user_token
            response["expiry"] = token_expiry
            response["message"] = "Token Generated Successfully!"
            
            return jsonify(response), 200
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error Auth Generate Controller! {e}"
            }
            return jsonify(response), 500
        
    @staticmethod
    def validate(data):
        
        try:
            
            req_params = ['token']
            
            for par in req_params:
                if par not in data.keys():
                    response = {
                        "code": 400,
                        "status": "failure",
                        "message": "Incomplete Request Body!"
                    }
                    return jsonify(response), 400
            
            user_token = data['token']
            
            res = UserToken.verify_token(user_token)
            
            if res['user_id'] == 0:
                response = {
                    "code": 401,
                    "status": "failure",
                    "message": "Token Expired!"
                }
                return jsonify(response), 401
            
            if res['user_id'] == -1:
                response = {
                    "code": 401,
                    "status": "failure",
                    "message": "Invalid Token!"
                }
                return jsonify(response), 401
            
            user_id = res['user_id']
            expiry = res['exp']
            
            cors_res = Middlewares.cors_check(user_id)
            
            if cors_res is not None:
                return cors_res
            
            existing_usertoken = User.query.filter_by(id=user_id).first().get_authtoken()
            
            if existing_usertoken != user_token:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Fresh Token Already Generated!"
                }
                return jsonify(response), 400
            
            response = {
                "code": 200,
                "status": "success",
                "token": user_token,
                "expiry": datetime.datetime.utcfromtimestamp(expiry),
                "message": "Valid User Token!"
            }
            
            return jsonify(response), 200
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error Auth Logout Controller! {e}"
            }
            return jsonify(response), 500

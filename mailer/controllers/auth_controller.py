from flask import jsonify, make_response
from mailer import db
import datetime
from mailer.models.user import User
from mailer.util.validator import Validator
from mailer.util.encryptor import Encryptor
from mailer.util.user_token import UserToken

class AuthController:

    @staticmethod
    def create(data):
        
        try:
        
            if data['password'] != data['confirm_password']:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Password and Confirm Password not Matched!"
                }
                return jsonify(response), 400
            
            if Validator.validate_email(data['email']) == False or Validator.validate_name(data['name']) == False or Validator.validate_password(data['password']) == False:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Data!"
                }
                return jsonify(response), 400
            
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "User already Exists!"
                }
                return jsonify(response), 400
            
            password_hash = Encryptor.encrypt_password(data['password'])
            
            new_user = User(
                name=data['name'],
                email=data['email'],
                password=password_hash
            )
            
            db.session.add(new_user)
            db.session.commit()
            
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
                "message": f"Error Auth Create Controller! {e}"
            }
            return jsonify(response), 500

    @staticmethod
    def generate(data):
        
        try:
            
            if Validator.validate_email(data['email']) == False or Validator.validate_password(data['password']) == False:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Data!"
                }
                return jsonify(response), 400
            
            existing_user = User.query.filter_by(email=data['email']).first()
            if not existing_user:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "User does not Exists!"
                }
                return jsonify(response), 400
            
            password_hash = existing_user.get_password_hash()
            
            if not Encryptor.verify_password(password_hash, data['password']) :
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Password!"
                }
                return jsonify(response), 400
            
            new_user = existing_user.to_dict()
            
            token_response = UserToken.generate_token(new_user['id'])
            
            if token_response == None:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Failed to Generate Token!"
                }
                return jsonify(response), 400
            
            existing_user.authtoken = token_response['token']
            db.session.commit()
            
            response = {}
            response['user'] = new_user
            response["status"] = "success"
            response["code"] = 200
            response["token"] = token_response['token']
            response["expiry"] = token_response['exp']
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
            
            existing_usertoken = User.query.filter_by(id=user_id).first().get_authtoken()
            
            if existing_usertoken != user_token:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Fresh Token Already Generated!"
                }
                return jsonify(response), 400
            
            response = make_response(
                    jsonify({
                    "code": 200,
                    "status": "success",
                    "token": user_token,
                    "expiry": datetime.datetime.utcfromtimestamp(expiry),
                    "message": "Valid User Token!"
                })
            )
            
            return response, 200
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error Auth Logout Controller! {e}"
            }
            return jsonify(response), 500

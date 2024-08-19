from flask import jsonify, make_response
from mailer import db
import datetime
from mailer.models.user import User
from mailer.util.validator import Validator
from mailer.util.encryptor import Encryptor
from mailer.util.user_token import UserToken

class AuthController:

    @staticmethod
    def signup(data):
        
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
            
            user_token = UserToken.generate_token(new_user.id)
            
            response_data = {}
            response_data['user'] = new_user.to_dict()
            response_data["status"] = "success"
            response_data["code"] = 201
            response_data["message"] = "User SignedUp Successfully!"
            
            response = make_response(jsonify(response_data), 201)
            
            response.set_cookie(
                "mailroom_user", 
                value=user_token, 
                max_age=datetime.timedelta(hours=29.5)
            )
            
            return response
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error Auth SignUp Controller! {e}"
            }
            return jsonify(response), 500

    @staticmethod
    def login(data):
        
        try:
            
            if Validator.validate_email(data['email']) == False or Validator.validate_password(data['password']) == False:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Data!"
                }
                return jsonify(response), 400
            
            existing_user = User.query.filter_by(email=data['email'],).first()
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
            
            user_token = UserToken.generate_token(new_user['id'])
            
            response_data = {}
            response_data['user'] = new_user
            response_data["status"] = "success"
            response_data["code"] = 200
            response_data["message"] = "User LoggedIn Successfully!"
            
            response = make_response(jsonify(response_data), 200)
            
            response.set_cookie(
                "mailroom_user", 
                value=user_token, 
                max_age=datetime.timedelta(hours=29.5)
            )
            
            return response
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error Auth Login Controller! {e}"
            }
            return jsonify(response), 500
        
    @staticmethod
    def logout():
        
        try:
            
            response = make_response(
                    jsonify({
                    "code": 200,
                    "status": "success",
                    "message": "User LoggedOut Successfully!"
                })
            )
            
            response.set_cookie('mailroom_user', '', expires=0)
            
            return response
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error Auth Logout Controller! {e}"
            }
            return jsonify(response), 500

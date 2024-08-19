from flask import jsonify, make_response, request
from mailer import db
import datetime
from mailer.models.user import User
from mailer.util.validator import Validator
from mailer.util.encryptor import Encryptor
from mailer.util.user_token import UserToken

class UserController:
    @staticmethod
    def get_users():
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

    @staticmethod
    def get_user(user_id):
        
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
            
            if isinstance(user_id, str):
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid UserID!"
                }
                return jsonify(response), 400
            
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
            
            if len(data['email']) > 0:
                if Validator.validate_email(data['email']) == False:
                    response = {
                        "code": 400,
                        "status": "failure",
                        "message": "Invalid Email!"
                    }
                    return jsonify(response), 400
            
            if Validator.validate_name(data['name']) == False:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Name!"
                }
                return jsonify(response), 400
            
            user = User.query.filter_by(id=user_id).first()
            
            if user.email != data['email']:           
                existing_user = User.query.filter_by(email=data['email']).first()
                if existing_user:
                    response = {
                        "code": 400,
                        "status": "failure",
                        "message": "Email already Exists!"
                    }
                    return jsonify(response), 400
            
            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)
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
        
            if data['new_password'] != data['confirm_password']:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "New Password and Confirm Password not Matched!"
                }
                return jsonify(response), 400
            
            if Validator.validate_password(data['current_password']) == False and Validator.validate_password(data['new_password']) == False and Validator.validate_password(data['confirm_password']) == False:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Password Validation Failed!"
                }
                return jsonify(response), 400
            
            user = User.query.filter_by(id=user_id).first()
            
            password_hash = user.get_password_hash()
            
            if not Encryptor.verify_password(password_hash, data['current_password']) :
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Current Password!"
                }
                return jsonify(response), 400
            
            data['new_password'] = Encryptor.encrypt_password(data['new_password'])
            
            user.password = data.get('new_password', user.password)
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
            
            if Validator.validate_password(data['password']) == False:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Password Validation Failed!"
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
            
            if not Encryptor.verify_password(password_hash, data['password']) :
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid User Password!"
                }
                return jsonify(response), 400
            
            db.session.delete(user)
            db.session.commit()
            
            response = make_response(
                    jsonify({
                    "code": 200,
                    "status": "success",
                    "message": "User Deleted Successfully!"
                }), 200
            )
            
            response.set_cookie('mailroom_user', '', expires=0)
            
            return response
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error User Delete Controller! {e}"
            }
            return jsonify(response), 500

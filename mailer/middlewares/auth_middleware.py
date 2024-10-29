from flask import request, jsonify, g
from mailer.models.user import User
from mailer.util.user_token import UserToken

class Middlewares:

    @staticmethod
    def authenticate_middleware():
        
        if request.method == 'OPTIONS':
            return None
        
        auth_header = request.headers.get('Authorization')

        if not auth_header or auth_header == None:
            response = {
                "code": 401,
                "status": "failure",
                "message": "Authorization Header Missing!"
            }
            return jsonify(response), 401

        token = auth_header.split(" ")[1] if " " in auth_header else None

        if not token:
            response = {
                "code": 401,
                "status": "failure",
                "message": "Token Missing in Authorization Header!"
            }
            return jsonify(response), 401

        decoded_token = UserToken.verify_token(token)

        if decoded_token['user_id'] == 0:
            response = {
                "code": 401,
                "status": "failure",
                "message": "Token Expired!"
            }
            return jsonify(response), 401
                
        if decoded_token['user_id'] == -1:
            response = {
                "code": 401,
                "status": "failure",
                "message": "Invalid Token!"
            }
            return jsonify(response), 401

        user_id = decoded_token['user_id']
            
        existing_usertoken = User.query.filter_by(id=user_id).first().get_authtoken()
            
        if existing_usertoken != token:
            response = {
                "code": 400,
                "status": "failure",
                "message": "Fresh Token Already Generated!"
            }
            return jsonify(response), 400
        
        g.user = user_id
        
        return None

from flask import request, jsonify, g
from mailer.util.user_token import UserToken

class Middlewares:

    @staticmethod
    def authenticate_middleware():
        
        auth_header = request.headers.get('Authorization')

        if not auth_header:
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

        g.user = decoded_token['user_id']
        
        return None


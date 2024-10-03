from flask import request, jsonify, g
from mailer.models.user import User
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
        
        cors_res = Middlewares.cors_check(g.user)
        
        if cors_res is not None:
            return cors_res
        
        return None
        
    
    def cors_check(user_id):
        
        origin = request.host
        if origin:
            user = User.query.filter_by(id=user_id).first()
            
            if not user:
                response = {
                    "code": 401,
                    "status": "failure",
                    "message": "Invalid Token!"
                }
                return jsonify(response), 401
            
            allowed_domain = user.get_userdomain()
            
            if origin != allowed_domain:
                response = {
                    "code": 403,
                    "status": "failure",
                    "message": "CORS Policy: Domain Not Allowed!"
                }
                return jsonify(response), 403
        else:
            response = {
                "code": 403,
                "status": "failure",
                "message": "Request Blocked: Failed to get request host!"
            }
            return jsonify(response), 403
        
        return None

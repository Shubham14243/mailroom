import jwt
import datetime
from flask import request, jsonify
from mailer.config.config import Config

class UserToken:
    
    @staticmethod
    def generate_token(user_id):
        
        secret_key = Config.TOKEN_KEY
        
        try:

            payload = {
                'user_id': user_id
            }
            
            token = jwt.encode(payload, secret_key, algorithm='HS256')
            
            return token
        
        except Exception as e:
            print(f"Error generating token: {e}")
            return None
    
    @staticmethod
    def verify_token():
        
        token = ''
        
        try:
            token = request.cookies.get('mailroom_user')
        except:
            response = {
                "code": 400,
                "status": "failure",
                "message": "Invalid Access!"
            }
            return jsonify(response), 400
        
        secret_key = Config.TOKEN_KEY
        
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return payload['user_id']
        
        except jwt.ExpiredSignatureError:
            return None
        
        except jwt.InvalidTokenError:
            return None

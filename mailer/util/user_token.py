import jwt
import datetime
from flask import request, jsonify
from mailer.config.config import Config

class UserToken:
    
    @staticmethod
    def generate_token(user_id):
        
        secret_key = Config.TOKEN_KEY
        
        token_expiry = datetime.datetime.utcnow() + datetime.timedelta(days=7)
        
        try:

            payload = {
                'user_id': user_id,
                'exp' : token_expiry
            }
            
            token = jwt.encode(payload, secret_key, algorithm='HS256')
            
            return {"token": token, "exp": token_expiry}
        
        except Exception as e:
            print(f"Error generating token: {e}")
            return None
    
    @staticmethod
    def verify_token(token):
        
        secret_key = Config.TOKEN_KEY
        
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return payload
        
        except jwt.ExpiredSignatureError:
            return {"user_id": 0}
        
        except jwt.InvalidTokenError:
            return {"user_id": -1}

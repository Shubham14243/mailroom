import hashlib
import random
import string
import base64

class ApiKey:
    
    @staticmethod
    def generate_api_key(user_id, app_id):
    
        random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        key_base = f"{user_id}:{app_id}:{random_part}"
        
        hash_object = hashlib.sha256(key_base.encode())
        api_key = base64.urlsafe_b64encode(hash_object.digest()[:15] + key_base.encode()).decode('utf-8')
        
        return api_key
    
    @staticmethod
    def verify_api_key(api_key):
        try:
            
            decoded_key = base64.urlsafe_b64decode(api_key.encode('utf-8'))
            key_str = decoded_key[15:].decode('utf-8')
            user_id, app_id, _ = key_str.split(':')
            
            return int(user_id), int(app_id)
        
        except:
            return None, None
    
from mailer import bcrypt

class Encryptor:
    
    @staticmethod
    def encrypt_password(password):
        
        hash = bcrypt.generate_password_hash(password, 8)
        
        return hash
        
    @staticmethod
    def verify_password(hash, password):
        
        result = bcrypt.check_password_hash(hash, password)
        
        return result        

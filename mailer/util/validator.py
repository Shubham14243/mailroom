import re

class Validator:
    
    @staticmethod
    def validate_email(email):
        
        pattern = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        expr = re.compile(pattern)

        if expr.fullmatch(email):
            return True
        else:
            return False
        
    @staticmethod
    def validate_name(name):
        
        if len(name) >= 3:
            return True
        return False
    
    @staticmethod
    def validate_password(password):
        
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$#!%*?&])[A-Za-z\d@$!%*?&]{5,20}$'
        expr = re.compile(pattern)
        
        if expr.fullmatch(password):
            return True
        else:
            return False
        
    def validate_subject(subject):
    
        MAX_LENGTH = 255
        pattern = r"^[a-zA-Z0-9\s\.,;:?!()'\"-]{3,255}$"

        if not isinstance(subject, str):
            return False

        if len(subject) > MAX_LENGTH:
            return False

        if not re.match(pattern, subject):
            return False

        return True

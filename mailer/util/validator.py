import re

class Validator:
    
    @staticmethod
    def validate_email(email):
        
        pattern = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        expr = re.compile(pattern)

        if expr.fullmatch(email):
            return None
        else:
            return 'Invalid Email!'
        
    @staticmethod
    def validate_name(name):
        
        if len(name) >= 3:
            return None
        return 'Invalid Name!'
    
    @staticmethod
    def validate_password(password):
        
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$#!%*?&])[A-Za-z\d@$!%*?&]{5,20}$'
        expr = re.compile(pattern)
        
        if expr.fullmatch(password):
            return None
        else:
            return 'Invalid Password! 5-20 Characters, 1 uppercase, 1 lowercase, 1special character(@$#!%*?&), 1 digit!'
        
    def validate_subject(subject):
    
        MAX_LENGTH = 255
        pattern = r"^[a-zA-Z0-9\s\.,;:?!()|'\"-]{3,255}$"

        if not isinstance(subject, str):
            return 'Invalid Subject! Not String!'

        if len(subject) > MAX_LENGTH:
            return 'Invalid Subject! Max Length Exceeded!'

        if not re.match(pattern, subject):
            return 'Invalid Subject! Allowed Characters .,;:?!()|\'"-!'

        return None
    
    def validate_domain(userdomain):
        pattern = r'^(https?:\/\/)(?:localhost|\d{1,3}(?:\.\d{1,3}){3}|[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z]{2,})+)(?::\d{1,5})?(?:\/[^\s]*)?$'
        expr = re.compile(pattern)

        if expr.fullmatch(userdomain):
            return None
        else:
            return 'Invalid Domain!'

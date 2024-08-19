import re

class HTMLParser:
    
    def text_body(body):
        
        MAX_LENGTH = 10000  # Adjust as needed
        pattern = r"^[\s\S]*$"

        if not isinstance(body, str):
            return False

        if len(body) > MAX_LENGTH:
            return False
        
        if not re.match(pattern, body):
            return False

        variable_pattern = r"\{\{[^{}]*\}\}"
        if not re.search(variable_pattern, body) and re.search(r"\{\{.*", body):
            return False
        
        open_braces = re.findall(r"\{\{", body)
        close_braces = re.findall(r"\}\}", body)

        if len(open_braces) != len(close_braces):
            return False

        return True
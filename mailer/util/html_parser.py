import re
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.valid = True

    def error(self, message):
        self.valid = False


class HTMLParser:
    
    def is_valid_text(body):
        
        MAX_LENGTH = 10000
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
    
    def is_valid_html(html_text):
        parser = MyHTMLParser()
        try:
            parser.feed(html_text)
            parser.close()
        except Exception:
            return False
        return parser.valid
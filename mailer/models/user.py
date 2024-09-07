from mailer import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    authtoken = db.Column(db.String(128))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
        
    def get_password_hash(self):
        return self.password
    
    def get_authtoken(self):
        return self.authtoken
    
    def __repr__(self):
        return f'<User {self.id}>'

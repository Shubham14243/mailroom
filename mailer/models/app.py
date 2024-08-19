from mailer import db
from datetime import datetime
    
class App(db.Model):
    app_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    app_name = db.Column(db.String(100), nullable=False)
    api_key = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('apps', lazy=True))

    def to_dict(self):
        return {
            'app_id': self.app_id,
            'app_name': self.app_name,
            'api_key': self.api_key,
            'created_at': self.created_at
        }

    def __repr__(self):
        return f'<App {self.app_id} by User {self.user_id}>'

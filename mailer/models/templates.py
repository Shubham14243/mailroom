from mailer import db
from datetime import datetime
    
class Templates(db.Model):
    template_id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('app.app_id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    sender_name = db.Column(db.String(128), nullable=False)
    sender_email = db.Column(db.String(128), nullable=False)
    subject = db.Column(db.String(128), nullable=False)
    body = db.Column(db.Text, nullable=True)
    is_html = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    app = db.relationship('App', backref=db.backref('templates', lazy=True))

    def to_dict(self):
        return {
            'template_id': self.template_id,
            'app_id': self.app_id,
            'name': self.name,
            'sender_name': self.sender_name,
            'sender_email': self.sender_email,
            'subject': self.subject,
            'body': self.body,
            'is_html': self.is_html,
            'created_at': self.created_at
        }

    def __repr__(self):
        return f'<Template {self.template_id} of App {self.app_id}>'

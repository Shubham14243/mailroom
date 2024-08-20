from mailer import db
from datetime import datetime

class MailLog(db.Model):
    log_id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('app.app_id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.template_id'), nullable=False)
    to_email = db.Column(db.String(128), nullable=False)
    from_email = db.Column(db.String(128), nullable=False)
    subject = db.Column(db.String(128), nullable=False)
    body_data = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    sent_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    app = db.relationship('App', backref=db.backref('logs', lazy=True))
    template = db.relationship('Templates', backref=db.backref('logs', lazy=True))

    def to_dict(self):
        return {
            'log_id': self.log_id,
            'app_id': self.app_id,
            'template_id': self.template_id,
            'to_email': self.to_email,
            'from_email': self.from_email,
            'subject': self.subject,
            'body_data': self.body_data,
            'status': self.status,
            'sent_at': self.sent_at
        }

    def __repr__(self):
        return f'<MailLog {self.log_id} for App {self.app_id}>'

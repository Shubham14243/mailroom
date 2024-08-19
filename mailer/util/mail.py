from mailer.config.config import Config
from mailer import mail
from flask_mail import Message
from flask import jsonify

class Mail:
    
    @staticmethod
    def send_mail():
        
        sender = "chatbit@admin.com"

        msg = Message(
            subject="Test Mail",
            sender="custom_sender@example.com",
            recipients=["srshristirajput999@gmail.com"],
            body="Hi!, this is test mail"
        )

        try:
            mail.send(msg)
            return jsonify({'message': 'Email sent successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        

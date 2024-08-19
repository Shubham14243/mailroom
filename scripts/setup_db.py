from mailer import create_app, db
from mailer.models.user import User

app = create_app()

with app.app_context():
    db.create_all()


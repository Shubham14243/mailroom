from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail
from mailer.config.config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
mail = Mail()
cors = CORS()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    bcrypt.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})
    migrate.init_app(app, db, directory='mailer/migrations')

    from mailer.views.user_view import bp as user_bp
    from mailer.views.auth_view import bp as auth_bp
    from mailer.views.app_view import bp as app_bp
    from mailer.views.templates_view import bp as template_bp
    from mailer.views.mail_view import bp as mail_bp
    
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(app_bp, url_prefix='/api/app')
    app.register_blueprint(template_bp, url_prefix='/api/template')
    app.register_blueprint(mail_bp, url_prefix='/api/mail')
    
    return app

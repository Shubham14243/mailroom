class Config:
    SECRET_KEY='6ph3apOqJy3DJVkOq65mOOpN4m1MdvHz'
    TOKEN_KEY='h8CgHPB25n'
    SQLALCHEMY_DATABASE_URI='sqlite:///mailer.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=587
    MAIL_USERNAME='guptashubham14243@gmail.com'
    MAIL_PASSWORD='tazuvjuejutnvfig'
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
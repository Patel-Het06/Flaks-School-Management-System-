import os

basedir = os.path.abspath(os.path.dirname(__file__))

class config():
    SECRET_KEY="mysecretkey"
    SQLALCHEMY_DATABASE_URI='sqlite:///'+ os.path.join(basedir , 'school.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS= False
    
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT= 587
    MAIL_USE_TLS=True
    MAIL_USERNAME='patel37983672@gmail.com'
    MAIL_PASSWORD='jiuzhlgkoihzzflg'
    MAIL_DEFAULT_SENDER='patel37983672@gmail.com'
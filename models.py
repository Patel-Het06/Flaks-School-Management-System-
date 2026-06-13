from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from extensions import db

class User(db.Model , UserMixin):
    __tablename__ = 'users'
    
    id=db.Column(db.Integer , primary_key=True)
    name=db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    mobile = db.Column(db.String(14), nullable=False)
    gender = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, default='user')
    is_verified = db.Column(db.Boolean, default=True)# chagne after otp verifivation
    otp = db.Column(db.String(6), nullable=True)
    otp_created_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, name,email,password,mobile,gender,role='user'):
        self.name=name
        self.email=email
        self.password=password
        self.mobile=mobile
        self.gender=gender
        self.role=role
        
    def __repr__(self):
        return f'{self.name} - {self.role}'
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SelectField,RadioField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Email,EqualTo,Length

class RegistrationForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired()])
    email=StringField('Email', validators=[ DataRequired() ,Email()])
    mobile=StringField('Mobile Number', validators=[DataRequired(), Length(min=10,max=10)])
    gender=RadioField('Gender', choices=[ ('Male', 'Male'),
                                         ('Female', 'Female') ],    validators=[DataRequired()])
    role=SelectField('Role', choices=[('user','User'),('admin','Admin')], validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    confirm_password=PasswordField('Confirm Password', validators=[EqualTo('password', message='Password must match!')])
    submit=SubmitField('Register')

class LoginForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=StringField('Password', validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')
    
class OTPForm(FlaskForm):
    otp = StringField("Enter OTP", validators=[DataRequired(), Length(min=6 , max=6)])
    submit= SubmitField('Verify OTP')
    
class UpdateProfileForm(FlaskForm):
    name=StringField('Full Name', validators=[DataRequired()])
    mobile= StringField('MObile No.' , validators=[DataRequired(),Length(min=10, max=10)])
    submit= SubmitField('Update Profile')
    
class ChangePasswordForm(FlaskForm):
    old_password=PasswordField('Old Password', validators=[DataRequired()])
    new_password=PasswordField('New Password', validators=[DataRequired(),Length(min=4)])
    confirm_password=PasswordField('Confirm New Password', validators=[DataRequired(),EqualTo('new_password',message='Password must match')])
    submit=SubmitField('Change Password')
    

    

    
    
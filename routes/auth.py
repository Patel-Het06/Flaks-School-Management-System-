from flask import Blueprint, flash, render_template, redirect, url_for, session
from forms import RegistrationForm, LoginForm, OTPForm, ForgotPasswordForm, ResetPassowrdForm
from extensions import db, mail
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from datetime import datetime, timedelta
import random

auth=Blueprint('auth',__name__) 

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    try:
        msg = Message(
        subject='🏫 School System - OTP Verification',
        recipients=[email],
        body=f'''
        Hello!

        Your OTP for School Management System is:

        {otp}

        This OTP will expire in 5 minutes.

        If you did not request this, please ignore this email.
        '''
    )
        mail.send(msg)
        print(f"✅ OTP sent to {email}")
        return True
    except Exception as e:
        print(f"❌ Email error: {e}")
        print(f"🔑 OTP is: {otp}")   # ← OTP will show in terminal
        return True                   # ← return True so registration continues



@auth.route('/')
def home():
    return render_template('home.html')

@auth.route('/register', methods=['GET','POST'])
def register():
    form=RegistrationForm()
    
    if form.validate_on_submit():
        existing_user=User.query.filter_by(email=form.email.data).first()
        
        if existing_user:
            flash('Email already exists! Please login.','danger')
            return redirect (url_for('auth.login'))
        
        hashed_password=generate_password_hash(form.password.data)
        
        new_user=User(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
            mobile=form.mobile.data,
            gender=form.gender.data,
            role=form.role.data
        )
        
        otp=generate_otp()
        new_user.otp= otp
        new_user.otp_created_at=datetime.utcnow()
        
        db.session.add(new_user)
        db.session.commit()
        
        send_otp_email(form.email.data, otp)
        
        session['verify_email']=form.email.data
        
        flash('OTP sent to your email! Please verify.', 'info') 
        return redirect(url_for('auth.verify_otp'))
    
    return render_template('auth/register.html', form=form)


@auth.route('/verify-opt' , methods=['GET', 'POST'])
def verify_otp():
    form = OTPForm()
    email = session.get('verify_email')

    if not email:
        flash('Session expired! Please register again.', 'danger')
        return redirect(url_for('auth.register'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()

        if not user:
            flash('User not found!', 'danger')
            return redirect(url_for('auth.register'))

        # check otp expiry (5 minutes)
        otp_age = datetime.utcnow() - user.otp_created_at
        if otp_age > timedelta(minutes=5):
            flash('OTP expired! Please register again.', 'danger')
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('auth.register'))

        # check otp match
        if form.otp.data != user.otp:
            flash('Wrong OTP! Please try again.', 'danger')
            return redirect(url_for('auth.verify_otp'))

        # otp verified
        user.is_verified = True
        user.otp = None
        user.otp_created_at = None
        db.session.commit()

        session.pop('verify_email', None)

        flash('Email verified successfully! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/otp.html', form=form)    

@auth.route('/resend-otp')
def resend_otp():
    email = session.get('verify_email')

    if not email:
        flash('Session expired! Please register again.', 'danger')
        return redirect(url_for('auth.register'))
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('auth.register'))
    
    otp=generate_otp()
    user.otp= otp
    user.otp_created_at=datetime.utcnow()
    db.session.commit()
    
    send_otp_email(email, otp)
    
    flash('New OTP sent to your email!', 'info')
    return redirect(url_for('auth.verify_otp'))
                              
@auth.route('/login' , methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
              
        if not user:
            flash('Email not found! Please register.', 'danger')
            return redirect(url_for('auth.register'))
        
        if  not user.is_verified:
            flash('Email not found! Please register.', 'danger')
            session['verify_email']= user.email
            return redirect(url_for('auth.verify_opt'))
        
        if not check_password_hash(user.password, form.password.data):
             flash('Wrong password! Please try again.', 'danger')
             return redirect(url_for('auth.login'))
         
        login_user(user, remember=form.remember.data)
        flash(f'Welcome back {user.name}!', 'success')
        
        if user.role =='user':
            return redirect(url_for('user.dashboard'))
            
        else:
            return redirect(url_for('admin.dashboard'))       
   
    return render_template('auth/login.html',form=form)

@auth.route('/forgot-password',methods=['GET', 'POST'])
def forgot_password():
    form=ForgotPasswordForm()
    
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        
        if not user:
            flash('Email not found!', 'danger')
            return redirect(url_for('auth.forgot_password'))
        
        otp=generate_otp()
        user.otp = otp
        user.otp_created_at= datetime.utcnow()
        db.session.commit()
        
        send_otp_email(form.email.data, otp)
        session['reset_email']= form.email.data
        
        flash('OTP sent to your email!', 'success')
        return redirect(url_for('auth.reset_password'))
    
    return render_template('auth/forgot_password.html', form=form)

@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    form=ResetPassowrdForm()
    email=session.get('reset_email')
    
    if not email:
        flash('Session expired!', 'danger')
        return redirect(url_for('auth.forgot_password'))
    
    if form.validate_on_submit():
        user=User.query.filter_by(email=email).first()
        
        if not user:
            flash('User not found!', 'danger')
            return redirect(url_for('auth.forgot_password'))
        
        otp_age=datetime.utcnow()- user.otp_created_at
        if otp_age> timedelta(minutes=5):
            flash('OTP expired! Try again.', 'danger')
            return redirect(url_for('auth.forgot_password'))
        
        if form.otp.data != user.otp:
            flash('Wrong OTP!', 'danger')
            return redirect(url_for('auth.reset_password'))
        
        user.password= generate_password_hash(form.new_password.data)
        user.otp= None
        user.otp_created_at=None
        db.session.commit()
        
        session.pop('reset_email', None)
        flash('Password reset successfully please login!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)



# djbbjkvmhbnbs

@auth.route('/resend-otp-for-reset-password')
def resend_otp_for_reset_password():
    email = session.get('reset_email')

    if not email:
        flash('Session expired! Please enter email again.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('auth.forgot_password'))
    
    otp=generate_otp()
    user.otp= otp
    user.otp_created_at=datetime.utcnow()
    db.session.commit()
    
    send_otp_email(email, otp)
    
    flash('New OTP sent to your email!', 'info')
    return redirect(url_for('auth.reset_password'))
    


@auth.route('/logout')
@login_required
def logout():
    logout_user()                                            
    flash('Logged out successfully!', 'success')
    return redirect(url_for('auth.home'))     

 

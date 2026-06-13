from flask import Blueprint , render_template, flash, redirect,url_for
from models import User
from extensions import db
from flask_login import login_required, current_user
from forms import UpdateProfileForm, ChangePasswordForm
from werkzeug.security import check_password_hash, generate_password_hash

user=Blueprint('user',__name__)

@user.route('/user/dashboard')
@login_required
def dashboard():
    
    # print("Current user:", current_user)           # ← add this
    # print("Current user role:", current_user.role) # ← add this
    # print("Is authenticated:", current_user.is_authenticated) # ← add this
    
    
    if current_user.role !='user':
        flash('Access Denied!', 'danger')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('user/dashboard.html')

@user.route('/user/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.role != 'user':
        flash('Access Denied!', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    form=UpdateProfileForm()
    
    if form.validate_on_submit():
        current_user.name=form.name.data
        current_user.mobile=form.mobile.data
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('user.profile'))
    
    form.name.data=current_user.name
    form.mobile.data=current_user.mobile
    
    return render_template('user/profile.html', form=form)

@user.route('/user/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if current_user.role !='user':
        flash('Access Denied!', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    form=ChangePasswordForm()
    
    if form.validate_on_submit():
        if not check_password_hash(current_user.password, form.old_password.data):
            flash('Old password is wrong', 'success')
            return redirect(url_for('user.change_password'))
        
        current_user.password= generate_password_hash(form.new_password.data)
        db.session.commit()
        flash('Password Change Successfully!', 'success')
        return redirect(url_for('user.profile'))
    
    return render_template('user/change_password.html', form=form)
    
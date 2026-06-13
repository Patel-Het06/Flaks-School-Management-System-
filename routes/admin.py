from flask import Blueprint, render_template, flash ,redirect,url_for
from models import User
from extensions import db
from flask_login import login_required, current_user
from forms import UpdateProfileForm

admin = Blueprint('admin', __name__)

@admin.route('/admin/dashboard')
@login_required
def dashboard():
    
    # print("Current user:", current_user)           # ← add this
    # print("Current user role:", current_user.role) # ← add this
    # print("Is authenticated:", current_user.is_authenticated) # ← add this
    
    if current_user.role != 'admin':
        flash('Access Denied!', 'danger')
        return redirect(url_for('user.dashboard'))
    all_users = User.query.filter(User.role != 'admin').all()
    
    return render_template('admin/dashboard.html', users=all_users)

@admin.route('/admin/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form=UpdateProfileForm()
    
    if form.validate_on_submit():
        current_user.name=form.name.data
        current_user.mobile=form.mobile.data
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('admin.profile'))
    
    form.name.data=current_user.name
    form.mobile.data=current_user.mobile
    
    return render_template('admin/profile.html', form=form)

@admin.route('/admin/delete/<int:id>')
@login_required
def delete_user(id):
    if current_user.role != 'admin':
        flash('Access Denied!', 'danger')
        return redirect(url_for('user.dashboard'))
    
    user=db.session.get(User,id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))
    
    
# app/routes/auth.py

from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models.user import User
from app.models.doctor import Doctor
from app.forms.auth_forms import LoginForm, RegistrationForm, ProfileEditForm, ChangePasswordForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """User login page."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact an administrator.', 'error')
                return render_template('auth/login.html', form=form)
            
            login_user(user, remember=form.remember_me.data)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            if not next_page:
                next_page = url_for('dashboard.index')
            
            flash(f'Welcome back, {user.get_full_name()}!', 'success')
            return redirect(next_page)
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('auth/login.html', form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """User registration page."""
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        
        # Handle doctor role
        if form.role.data == 'doctor':
            if form.doctor_id.data == 0:
                # Create new doctor profile
                doctor = Doctor(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    specialty='General Practitioner',  # Default, can be changed later
                    phone=form.phone.data,
                    email=form.email.data
                )
                db.session.add(doctor)
                db.session.flush()  # Get the doctor ID
                user.doctor_id = doctor.id
            else:
                # Link to existing doctor profile
                user.doctor_id = form.doctor_id.data
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Registration successful! Welcome, {user.get_full_name()}!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    """User logout."""
    username = current_user.username
    logout_user()
    flash(f'You have been logged out successfully, {username}.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route("/profile")
@login_required
def profile():
    """User profile page."""
    return render_template('auth/profile.html', user=current_user)


@auth_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    """Edit user profile."""
    form = ProfileEditForm(current_user, obj=current_user)
    
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Your profile has been updated successfully!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/edit_profile.html', form=form)


@auth_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change user password."""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            current_user.updated_at = datetime.utcnow()
            db.session.commit()
            
            flash('Your password has been changed successfully!', 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Current password is incorrect.', 'error')
    
    return render_template('auth/change_password.html', form=form)

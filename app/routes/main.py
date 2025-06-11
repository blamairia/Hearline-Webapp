# app/routes/main.py

from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required, current_user
from app.decorators.auth import any_role_required

main_bp = Blueprint('main', __name__)


@main_bp.route("/")
@login_required
def index():
    """Redirect to dashboard."""
    return redirect(url_for('dashboard.index'))


@main_bp.route("/settings")
@login_required
@any_role_required
def settings():
    """Settings page with clinic information and doctor management."""
    from app.models.settings import ClinicInfo, GeneralSettings
    from app.models.doctor import Doctor
    
    # Get existing clinic info and settings
    clinic_info = ClinicInfo.query.first()
    general_settings = GeneralSettings.query.first()
    
    # Get all doctors for the doctor management tab
    doctors = Doctor.query.order_by(Doctor.last_name, Doctor.first_name).all()
    
    return render_template('pages/settings.html',
                         clinic_info=clinic_info,
                         general_settings=general_settings,
                         doctors=doctors)

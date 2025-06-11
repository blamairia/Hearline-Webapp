# app/routes/dashboard.py

from datetime import date, datetime, timedelta
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.decorators.auth import doctor_required, assistant_required
from app.models.patient import Patient
from app.models.visit import Visit
from app.models.appointment import Appointment
from app.extensions import db

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route("/")
@login_required
def index():
    """Main dashboard - role-specific content."""
    # Get basic statistics
    total_patients = Patient.query.count()
    total_visits = Visit.query.count()
    total_appointments = Appointment.query.count()
    
    # Today's statistics
    today = date.today()
    today_visits = Visit.query.filter(
        db.func.date(Visit.visit_date) == today
    ).count()
    
    today_appointments = Appointment.query.filter(
        db.func.date(Appointment.date) == today,
        Appointment.state == 'scheduled'
    ).count()
    
    # Recent activity based on role
    if current_user.is_doctor():
        # Doctor-specific dashboard data
        recent_visits = Visit.query.filter(
            Visit.doctor_id == current_user.doctor_id
        ).order_by(Visit.visit_date.desc()).limit(5).all()
        
        doctor_appointments = Appointment.query.filter(
            Appointment.doctor_id == current_user.doctor_id,
            Appointment.date >= datetime.now()
        ).order_by(Appointment.date).limit(5).all()
        
        return render_template('dashboard/doctor_dashboard.html',
                             total_patients=total_patients,
                             total_visits=total_visits,
                             total_appointments=total_appointments,
                             today_visits=today_visits,
                             today_appointments=today_appointments,
                             recent_visits=recent_visits,
                             upcoming_appointments=doctor_appointments)
    else:
        # Assistant dashboard - general overview
        recent_visits = Visit.query.order_by(Visit.visit_date.desc()).limit(5).all()
        upcoming_appointments = Appointment.query.filter(
            Appointment.date >= datetime.now()
        ).order_by(Appointment.date).limit(5).all()
        
        return render_template('dashboard/assistant_dashboard.html',
                             total_patients=total_patients,
                             total_visits=total_visits,
                             total_appointments=total_appointments,
                             today_visits=today_visits,
                             today_appointments=today_appointments,
                             recent_visits=recent_visits,
                             upcoming_appointments=upcoming_appointments)


# Dashboard API Endpoints
@dashboard_bp.route('/api/doctor/stats')
@login_required
@doctor_required
def doctor_dashboard_stats():
    """Get doctor dashboard statistics."""
    try:
        week_ago = datetime.now() - timedelta(days=7)
        today = date.today()
        
        # Get doctor's statistics
        doctor_patients = Patient.query.join(Visit).filter(
            Visit.doctor_id == current_user.doctor_id
        ).distinct().count()
        
        today_visits = Visit.query.filter(
            Visit.doctor_id == current_user.doctor_id,
            db.func.date(Visit.visit_date) == today
        ).count()
        
        ecg_tests_week = Visit.query.filter(
            Visit.doctor_id == current_user.doctor_id,
            Visit.visit_date >= week_ago,
            Visit.ecg_prediction.isnot(None)
        ).count()
        
        # Mock additional statistics
        avg_visit_time = 45  # minutes
        patients_change = 5.2
        visits_change = 12.5
        ecg_change = 8.7
        time_change = -3.2
        
        return jsonify({
            'total_patients': doctor_patients,
            'today_visits': today_visits,
            'ecg_tests_week': ecg_tests_week,
            'avg_visit_time': avg_visit_time,
            'patients_change': patients_change,
            'visits_change': visits_change,
            'ecg_change': ecg_change,
            'time_change': time_change
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@dashboard_bp.route('/api/assistant/stats')
@login_required
@assistant_required
def assistant_dashboard_stats():
    """Get assistant dashboard statistics."""
    try:
        today = date.today()
        week_ago = datetime.now() - timedelta(days=7)
        
        total_patients = Patient.query.count()
        today_appointments = Appointment.query.filter(
            db.func.date(Appointment.date) == today
        ).count()
        pending_visits = Appointment.query.filter_by(state='scheduled').count()
        completed_today = Visit.query.filter(
            db.func.date(Visit.visit_date) == today
        ).count()
        
        return jsonify({
            'total_patients': total_patients,
            'today_appointments': today_appointments,
            'pending_visits': pending_visits,
            'completed_today': completed_today
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@dashboard_bp.route('/api/recent-activity')
@login_required
def dashboard_recent_activity():
    """Get recent activity for dashboard."""
    try:
        activities = []
        
        # Recent patients (last 3)
        recent_patients = Patient.query.order_by(Patient.created_at.desc()).limit(3).all()
        for patient in recent_patients:
            activities.append({
                'type': 'patient_added',
                'title': f'New patient registered: {patient.first_name} {patient.last_name}',
                'timestamp': patient.created_at.isoformat()
            })
        
        # Recent visits (last 3)
        recent_visits = Visit.query.order_by(Visit.visit_date.desc()).limit(3).all()
        for visit in recent_visits:
            activities.append({
                'type': 'visit_completed',
                'title': f'Visit completed for {visit.patient.first_name} {visit.patient.last_name}',
                'timestamp': visit.visit_date.isoformat()
            })
        
        # Sort by timestamp descending
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return jsonify(activities[:10])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

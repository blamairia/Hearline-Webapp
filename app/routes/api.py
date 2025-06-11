# app/routes/api.py

from datetime import date, datetime, timedelta
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from sqlalchemy import or_, desc
from app.decorators.auth import any_role_required, doctor_required, assistant_required
from app.extensions import db
from app.models.patient import Patient
from app.models.visit import Visit
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.user import User
from app.models.prescription import Medicament

api_bp = Blueprint('api', __name__)


# --- Patients API ---
@api_bp.route('/patients')
@login_required
@any_role_required
def api_patients():
    """API endpoint to get patient data for tables."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '', type=str).strip()
        
        query = Patient.query
        
        # Filter by search term (first or last name)
        if search:
            pattern = f'%{search}%'
            query = query.filter(
                or_(
                    Patient.first_name.ilike(pattern),
                    Patient.last_name.ilike(pattern)
                )
            )
        
        # Paginate results
        patients_paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Serialize results
        patients = [
            {
                'id': p.id,
                'first_name': p.first_name,
                'last_name': p.last_name,
                'date_of_birth': p.date_of_birth.strftime('%Y-%m-%d') if p.date_of_birth else None,
                'gender': p.gender,
                'phone': p.phone,
                'email': p.email,
                'created_at': p.created_at.strftime('%Y-%m-%d %H:%M'),
                'visits_count': p.visits.count()
            }
            for p in patients_paginated.items
        ]
        
        return jsonify({
            'patients': patients,
            'pagination': {
                'page': patients_paginated.page,
                'per_page': patients_paginated.per_page,
                'total': patients_paginated.total,
                'pages': patients_paginated.pages
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# --- Doctors API ---
@api_bp.route('/doctors')
@login_required
@any_role_required
def api_doctors():
    """API endpoint to get doctor data."""
    try:
        doctors = Doctor.query.order_by(Doctor.last_name, Doctor.first_name).all()
        doctor_list = [
            {
                'id': d.id,
                'first_name': d.first_name,
                'last_name': d.last_name,
                'specialty': d.specialty,
                'phone': d.phone,
                'email': d.email,
                'user_id': d.user.id if d.user else None,
                'username': d.user.username if d.user else None
            }
            for d in doctors
        ]
        return jsonify({'doctors': doctor_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# --- Visits API ---
@api_bp.route('/visits')
@login_required
@any_role_required
def api_visits():
    """API endpoint to get visit data for tables."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '', type=str).strip()
        
        query = Visit.query
        
        # Filter by search term (patient name, diagnosis, etc.)
        if search:
            pattern = f'%{search}%'
            query = query.filter(
                or_(
                    Patient.first_name.ilike(pattern),
                    Patient.last_name.ilike(pattern),
                    Visit.diagnosis.ilike(pattern)
                )
            ).join(Patient)  # Join with Patient table for name search
        
        # Paginate results
        visits_paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Serialize results
        visits = [
            {
                'id': v.id,
                'patient_name': f"{v.patient.first_name} {v.patient.last_name}",
                'visit_date': v.visit_date.strftime('%Y-%m-%d %H:%M') if v.visit_date else None,
                'diagnosis': v.diagnosis,
                'payment_status': v.payment_status,
                'created_at': v.created_at.strftime('%Y-%m-%d %H:%M'),
                'prescriptions_count': v.prescriptions.count(),
                'documents_count': v.documents.count()
            }
            for v in visits_paginated.items
        ]
        
        return jsonify({
            'visits': visits,
            'pagination': {
                'page': visits_paginated.page,
                'per_page': visits_paginated.per_page,
                'total': visits_paginated.total,
                'pages': visits_paginated.pages
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# --- Appointments API ---
@api_bp.route('/appointments')
@login_required
@any_role_required
def api_appointments():
    """API endpoint to get appointment data for tables."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '', type=str).strip()
        
        query = Appointment.query
        
        # Filter by search term (patient name, doctor name, reason, etc.)
        if search:
            pattern = f'%{search}%'
            query = query.filter(
                or_(
                    Patient.first_name.ilike(pattern),
                    Patient.last_name.ilike(pattern),
                    Doctor.first_name.ilike(pattern),
                    Doctor.last_name.ilike(pattern),
                    Appointment.reason.ilike(pattern)
                )
            ).join(Patient, Doctor)  # Join with Patient and Doctor tables
        
        # Paginate results
        appointments_paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Serialize results
        appointments = [
            {
                'id': a.id,
                'patient_name': f"{a.patient.first_name} {a.patient.last_name}",
                'doctor_name': f"Dr. {a.doctor.first_name} {a.doctor.last_name}" if a.doctor else "No doctor assigned",
                'date': a.date.strftime('%Y-%m-%d %H:%M') if a.date else None,
                'reason': a.reason,
                'state': a.state,
                'created_at': a.created_at.strftime('%Y-%m-%d %H:%M')
            }
            for a in appointments_paginated.items
        ]
        
        return jsonify({
            'appointments': appointments,
            'pagination': {
                'page': appointments_paginated.page,
                'per_page': appointments_paginated.per_page,
                'total': appointments_paginated.total,
                'pages': appointments_paginated.pages
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# --- Medicaments API ---
@api_bp.route('/medicaments/search')
@login_required
@any_role_required
def search_medicaments():
    """AJAX endpoint to search medicaments by name."""
    try:
        q = request.args.get('q', '', type=str).strip()
        page = request.args.get('page', 1, type=int)
        per_page = 10
        
        query = Medicament.query
        if q:
            pattern = f"%{q}%"
            query = query.filter(
                or_(
                    Medicament.nom_com.ilike(pattern),
                    Medicament.nom_dci.ilike(pattern)
                )
            )
        
        paginated = query.order_by(Medicament.nom_com).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        results = [
            {
                'id': med.num_enr,
                'text': f"{med.nom_com} ({med.dosage}{med.unite})" if med.dosage and med.unite else med.nom_com,
                'nom_com': med.nom_com,
                'dosage': med.dosage,
                'unite': med.unite
            }
            for med in paginated.items
        ]
        
        more = paginated.pages > page
        return jsonify({'medicaments': results, 'pagination': {'more': more}})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# --- Dashboard API endpoints ---
@api_bp.route('/dashboard/visits-chart')
@login_required
def dashboard_visits_chart():
    """Get visits chart data for last 7 days."""
    try:
        today = date.today()
        dates = []
        visits_count = []
        
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            dates.append(day.strftime('%m/%d'))
            
            # Count visits for this day
            count = Visit.query.filter(
                db.func.date(Visit.visit_date) == day
            ).count()
            visits_count.append(count)
        
        return jsonify({
            'labels': dates,
            'visits': visits_count
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/dashboard/patient-queue')
@login_required
def dashboard_patient_queue():
    """Get patient queue for assistant dashboard."""
    try:
        today = date.today()
        
        # Get today's appointments that are scheduled or in progress
        appointments = Appointment.query.filter(
            db.func.date(Appointment.date) == today,
            Appointment.state.in_(['scheduled', 'in_progress'])
        ).order_by(Appointment.date).all()
        
        queue = []
        for apt in appointments:
            status = 'waiting' if apt.state == 'scheduled' else 'in-progress'
            queue.append({
                'name': f"{apt.patient.first_name} {apt.patient.last_name}",
                'visit_type': apt.purpose or 'General Visit',
                'scheduled_time': apt.date.isoformat(),
                'status': status
            })
        
        return jsonify(queue)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/dashboard/today-schedule')
@login_required
def dashboard_today_schedule():
    """Get today's schedule for dashboard."""
    try:
        today = date.today()
        
        appointments = Appointment.query.filter(
            db.func.date(Appointment.date) == today,
            Appointment.state == 'scheduled'
        ).order_by(Appointment.date).limit(10).all()
        
        schedule = []
        for apt in appointments:
            schedule.append({
                'time': apt.date.isoformat(),
                'patient_name': f"{apt.patient.first_name} {apt.patient.last_name}",
                'visit_type': apt.purpose or 'General Visit'
            })
        
        return jsonify(schedule)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/dashboard/notifications')
@login_required
def dashboard_notifications():
    """Get notifications for dashboard."""
    try:
        notifications = []
        
        # Mock notifications - in a real app, these would come from a notifications table
        notifications = [
            {
                'type': 'appointment',
                'title': 'Upcoming appointment in 30 minutes',
                'timestamp': (datetime.now() - timedelta(minutes=10)).isoformat()
            },
            {
                'type': 'patient',
                'title': 'New patient registration pending approval',
                'timestamp': (datetime.now() - timedelta(hours=1)).isoformat()
            },
            {
                'type': 'system',
                'title': 'System backup completed successfully',
                'timestamp': (datetime.now() - timedelta(hours=2)).isoformat()
            }
        ]
        
        return jsonify(notifications)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

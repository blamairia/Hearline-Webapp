# app/routes/appointments.py

from datetime import date, datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from sqlalchemy import or_
from app.decorators.auth import any_role_required
from app.extensions import db
from app.models.appointment import Appointment
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.visit import Visit
from app.forms.appointment_forms import AppointmentForm

appointments_bp = Blueprint('appointments', __name__)


@appointments_bp.route("/new", methods=["GET", "POST"])
@login_required
@any_role_required
def create_appointment():
    """Create a new appointment."""
    form = AppointmentForm()
    
    # Populate patient choices
    patients = Patient.query.order_by(Patient.last_name, Patient.first_name).all()
    form.patient_id.choices = [
        (p.id, f"{p.first_name} {p.last_name}")
        for p in patients
    ]
    
    # Populate doctor choices
    doctors = Doctor.query.order_by(Doctor.last_name, Doctor.first_name).all()
    form.doctor_id.choices = [(None, "No doctor assigned")] + [
        (d.id, f"Dr. {d.first_name} {d.last_name} - {d.specialty}")
        for d in doctors
    ]

    if form.validate_on_submit():
        try:
            appointment = Appointment(
                patient_id=form.patient_id.data,
                doctor_id=form.doctor_id.data,
                date=form.date.data,
                reason=form.reason.data,
                state=form.state.data
            )
            
            db.session.add(appointment)
            db.session.commit()
            
            flash(f'Appointment scheduled successfully for {appointment.patient.first_name} {appointment.patient.last_name}!', 'success')
            return redirect(url_for('appointments.appointments_table'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error scheduling appointment: {str(e)}', 'error')
    
    return render_template('forms/appointment_form.html', form=form)


@appointments_bp.route("/")
@login_required
@any_role_required
def appointments_table():
    """Display comprehensive appointments table with filtering and sorting capabilities."""
    # Get all appointments with their related data
    appointments = Appointment.query.order_by(Appointment.date.desc()).all()
    
    # Get all doctors for the filter dropdown
    doctors = Doctor.query.order_by(Doctor.last_name, Doctor.first_name).all()
    
    # Calculate appointment statistics
    stats = {
        'total': Appointment.query.count(),
        'scheduled': Appointment.query.filter_by(state='scheduled').count(),
        'completed': Appointment.query.filter_by(state='completed').count(),
        'today': Appointment.query.filter(
            db.func.date(Appointment.date) == date.today()
        ).count()
    }
    
    return render_template("tables/appointments_table.html", 
                         appointments=appointments,
                         doctors=doctors,
                         stats=stats,
                         date=date,
                         datetime=datetime)


@appointments_bp.route("/<int:appointment_id>/edit", methods=["GET", "POST"])
@login_required
@any_role_required
def edit_appointment(appointment_id):
    """Edit an existing appointment."""
    appointment = Appointment.query.get_or_404(appointment_id)
    form = AppointmentForm(obj=appointment)
    
    # Populate patient choices
    patients = Patient.query.order_by(Patient.last_name, Patient.first_name).all()
    form.patient_id.choices = [
        (p.id, f"{p.first_name} {p.last_name}")
        for p in patients
    ]
    
    # Populate doctor choices
    doctors = Doctor.query.order_by(Doctor.last_name, Doctor.first_name).all()
    form.doctor_id.choices = [(None, "No doctor assigned")] + [
        (d.id, f"Dr. {d.first_name} {d.last_name} - {d.specialty}")
        for d in doctors
    ]

    if form.validate_on_submit():
        try:
            appointment.patient_id = form.patient_id.data
            appointment.doctor_id = form.doctor_id.data
            appointment.date = form.date.data
            appointment.reason = form.reason.data
            appointment.state = form.state.data
            
            db.session.commit()
            
            flash('Appointment updated successfully!', 'success')
            return redirect(url_for('appointments.appointments_table'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating appointment: {str(e)}', 'error')
    
    return render_template('forms/appointment_form.html', form=form, appointment=appointment)


@appointments_bp.route("/api/<int:appointment_id>/update-status", methods=["POST"])
@login_required
@any_role_required
def update_appointment_status(appointment_id):
    """Update appointment status via API."""
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        data = request.get_json()
        
        new_status = data.get('status')
        if new_status not in ['scheduled', 'completed', 'canceled']:
            return jsonify({'success': False, 'message': 'Invalid status'}), 400
        
        appointment.state = new_status
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Appointment status updated to {new_status}'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@appointments_bp.route("/api/<int:appointment_id>/create-visit", methods=["POST"])
@login_required
@any_role_required
def create_visit_from_appointment(appointment_id):
    """Create a visit from an appointment."""
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        
        # Check if visit already exists
        if appointment.visit:
            return jsonify({'success': False, 'message': 'Visit already exists for this appointment'}), 400
        
        # Create new visit
        visit = Visit(
            visit_date=appointment.date.date(),
            patient_id=appointment.patient_id,
            chief_complaint=appointment.reason,
            appointment_id=appointment.id
        )
        
        db.session.add(visit)
        appointment.state = 'completed'
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Visit created successfully',
            'visit_id': visit.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@appointments_bp.route("/api/<int:appointment_id>", methods=["DELETE"])
@login_required
@any_role_required
def delete_appointment(appointment_id):
    """Delete an appointment."""
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        
        # Check if appointment has an associated visit
        if appointment.visit:
            return jsonify({'success': False, 'message': 'Cannot delete appointment with associated visit'}), 400
        
        patient_name = f"{appointment.patient.first_name} {appointment.patient.last_name}"
        
        db.session.delete(appointment)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Appointment for {patient_name} has been deleted'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

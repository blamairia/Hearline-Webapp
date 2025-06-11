# app/routes/patients.py

from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from sqlalchemy import or_
from app.decorators.auth import any_role_required
from app.extensions import db
from app.models.patient import Patient
from app.models.visit import Visit
from app.models.prescription import Prescription
from app.forms.patient_forms import PatientForm
from app.services.patient_service import PatientService

patients_bp = Blueprint('patients', __name__)


@patients_bp.route("/new", methods=["GET", "POST"])
@login_required
@any_role_required
def create_patient():
    """Create a new patient."""
    form = PatientForm()
    if form.validate_on_submit():
        # Check if patient already exists
        if PatientService.check_patient_exists(form.first_name.data, form.last_name.data):
            flash('A patient with this name already exists.', 'error')
            return render_template("forms/patient_form.html", form=form)
        
        try:
            patient_data = {
                'first_name': form.first_name.data,
                'last_name': form.last_name.data,
                'date_of_birth': form.date_of_birth.data,
                'gender': form.gender.data,
                'address': form.address.data,
                'phone': form.phone.data,
                'email': form.email.data,
                'medical_history': form.medical_history.data,
            }
            
            patient = PatientService.create_patient(patient_data)
            flash("Patient created successfully!", "success")
            return redirect(url_for("patients.patient_details", patient_id=patient.id))
            
        except Exception as e:
            flash(f"Error creating patient: {str(e)}", "error")

    return render_template("forms/patient_form.html", form=form)


@patients_bp.route("/")
@login_required
@any_role_required
def patients_table():
    """Display comprehensive patients table with filtering and sorting capabilities."""
    # Get all patients with their related data
    patients = Patient.query.order_by(Patient.last_name, Patient.first_name).all()
    
    return render_template("tables/patients_table.html", 
                         patients=patients,
                         Patient=Patient,
                         Visit=Visit,
                         Prescription=Prescription,
                         date=date)


@patients_bp.route("/<int:patient_id>")
@login_required
@any_role_required
def patient_details(patient_id):
    """Display patient details page."""
    patient = PatientService.get_patient_by_id(patient_id)
    visits = patient.visits.order_by(Visit.visit_date.desc()).all()
    
    return render_template("patient_details.html", 
                         patient=patient, 
                         visits=visits,
                         date=date)


@patients_bp.route("/<int:patient_id>/edit", methods=["GET", "POST"])
@login_required
@any_role_required
def edit_patient(patient_id):
    """Edit patient information."""
    patient = PatientService.get_patient_by_id(patient_id)
    form = PatientForm(obj=patient)
    
    if form.validate_on_submit():
        # Check if patient with same name exists (excluding current patient)
        if PatientService.check_patient_exists(form.first_name.data, form.last_name.data, exclude_id=patient_id):
            flash('A patient with this name already exists.', 'error')
            return render_template("forms/patient_form.html", form=form, patient=patient)
        
        try:
            patient_data = {
                'first_name': form.first_name.data,
                'last_name': form.last_name.data,
                'date_of_birth': form.date_of_birth.data,
                'gender': form.gender.data,
                'address': form.address.data,
                'phone': form.phone.data,
                'email': form.email.data,
                'medical_history': form.medical_history.data,
            }
            
            PatientService.update_patient(patient_id, patient_data)
            flash("Patient updated successfully!", "success")
            return redirect(url_for("patients.patient_details", patient_id=patient.id))
            
        except Exception as e:
            flash(f"Error updating patient: {str(e)}", "error")

    return render_template("forms/patient_form.html", form=form, patient=patient)


@patients_bp.route("/search")
@login_required
@any_role_required
def search_patients():
    """AJAX endpoint to search patients for searchable dropdown."""
    try:
        q = request.args.get('q', '', type=str).strip()
        page = request.args.get('page', 1, type=int)
        per_page = 10
        
        paginated = PatientService.search_patients(q, page, per_page)
        
        results = [
            {
                'id': p.id,
                'text': f"{p.first_name} {p.last_name}",
                'first_name': p.first_name or '',
                'last_name': p.last_name or '',
                'phone': p.phone or '',
                'email': p.email or ''
            }
            for p in paginated.items
        ]
        
        more = paginated.pages > page
        return jsonify({'patients': results, 'pagination': {'more': more}})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@patients_bp.route("/create", methods=['POST'])
@login_required
@any_role_required
def create_patient_ajax():
    """AJAX endpoint to create a new patient."""
    try:
        data = request.get_json()
        
        # Validate required fields
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        
        if not first_name or not last_name:
            return jsonify({'error': 'First name and last name are required'}), 400
        
        # Check if patient already exists
        if PatientService.check_patient_exists(first_name, last_name):
            return jsonify({'error': 'Patient with this name already exists'}), 400
          # Create new patient
        patient_data = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': data.get('phone', '').strip() or None,
            'email': data.get('email', '').strip() or None,
            'address': data.get('address', '').strip() or None,
            'date_of_birth': None,  # Can be added later
            'gender': 'Other'  # Default value, can be updated later
        }
        
        new_patient = PatientService.create_patient(patient_data)
        
        return jsonify({
            'success': True,
            'patient': {
                'id': new_patient.id,
                'text': f"{new_patient.first_name} {new_patient.last_name}",
                'first_name': new_patient.first_name,
                'last_name': new_patient.last_name,
                'phone': new_patient.phone or '',
                'email': new_patient.email or ''
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

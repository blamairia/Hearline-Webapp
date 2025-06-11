# app/routes/visits.py

from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from sqlalchemy import desc, or_
from app.decorators.auth import any_role_required
from app.extensions import db
from app.models.visit import Visit, VisitDocument
from app.models.patient import Patient
from app.models.prescription import Prescription, Medicament
from app.forms.visit_forms import VisitForm
from app.services.visit_service import VisitService
from app.utils.helpers import save_uploaded_file

visits_bp = Blueprint('visits', __name__)


@visits_bp.route("/new", methods=["GET", "POST"])
@login_required
@any_role_required
def create_visit():
    """Render VisitForm, handle nested prescriptions & documents, save Visit with child rows."""
    form = VisitForm()
    
    # Populate choices for prescriptions (medicaments)
    medicaments = Medicament.query.order_by(Medicament.nom_com).all()
    medicament_choices = [
        (med.num_enr, f"{med.nom_com} ({med.dosage}{med.unite})" if med.dosage and med.unite else med.nom_com)
        for med in medicaments
    ]
    
    for pres_sub in form.prescriptions:
        pres_sub.medicament_num_enr.choices = medicament_choices

    if form.validate_on_submit():
        try:
            visit_service = VisitService()
            
            # Prepare visit data
            visit_data = {
                'patient_id': form.patient_id.data,
                'visit_date': form.visit_date.data,
                'diagnosis': form.diagnosis.data,
                'follow_up_date': form.follow_up_date.data,
                'payment_total': form.payment_total.data,
                'payment_status': form.payment_status.data,
                'payment_remaining': form.payment_remaining.data,
            }
            
            # Handle ECG file uploads
            if form.ecg_mat.data:
                visit_data['ecg_mat'] = save_uploaded_file(form.ecg_mat.data, 'ecg')
            if form.ecg_hea.data:
                visit_data['ecg_hea'] = save_uploaded_file(form.ecg_hea.data, 'ecg')
            
            # Prepare prescriptions data
            prescriptions_data = []
            for pres_sub in form.prescriptions:
                if pres_sub.medicament_num_enr.data and pres_sub.dosage_instructions.data:
                    prescriptions_data.append({
                        'medicament_num_enr': pres_sub.medicament_num_enr.data,
                        'dosage_instructions': pres_sub.dosage_instructions.data,
                        'quantity': pres_sub.quantity.data,
                    })
            
            # Prepare documents data
            documents_data = []
            for doc_sub in form.documents:
                if doc_sub.file_path.data:
                    file_path = save_uploaded_file(doc_sub.file_path.data, 'docs')
                    if file_path:
                        documents_data.append({
                            'doc_type': doc_sub.doc_type.data,
                            'file_path': file_path,
                            'notes': doc_sub.notes.data,
                        })
            
            # Create visit
            visit = visit_service.create_visit(visit_data, prescriptions_data, documents_data)
            
            # Try ECG analysis if files were uploaded
            if visit.has_ecg_files():
                try:
                    visit_service.analyze_visit_ecg(visit.id)
                    flash("ECG inference completed automatically.", "info")
                except Exception as e:
                    flash(f"ECG inference failed: {e}", "warning")

            flash("Visit created successfully!", "success")
            return redirect(url_for("visits.visit_details", visit_id=visit.id))
            
        except Exception as e:
            flash(f"Error creating visit: {str(e)}", "error")

    return render_template("forms/visit_form.html", form=form)


@visits_bp.route("/")
@login_required
@any_role_required
def visits_table():
    """Display comprehensive visits table with filtering and sorting capabilities."""
    # Get all visits with their related data, ordered by visit date (newest first)
    visits = Visit.query.order_by(desc(Visit.visit_date)).all()
    
    return render_template("tables/visits_table.html", 
                         visits=visits,
                         Patient=Patient,
                         Visit=Visit,
                         Prescription=Prescription,
                         VisitDocument=VisitDocument,
                         date=date)


@visits_bp.route("/<int:visit_id>")
@login_required
@any_role_required
def visit_details(visit_id):
    """Display comprehensive visit details including ECG analysis, prescriptions, and documents."""
    visit_service = VisitService()
    visit = visit_service.get_visit_by_id(visit_id)
    
    # Get related data
    prescriptions = visit.prescriptions.all()
    documents = visit.documents.all()
    
    # Prepare ECG analysis data if available
    ecg_analysis = None
    if visit.has_ecg_prediction():
        primary_diagnosis = visit.get_primary_diagnosis()
        
        ecg_analysis = {
            "probabilities": visit.ecg_prediction,
            "class_names": visit_service.ecg_service.class_names,
            "primary_diagnosis": primary_diagnosis
        }
    
    return render_template("visit_details.html", 
                         visit=visit, 
                         prescriptions=prescriptions, 
                         documents=documents,
                         ecg_analysis=ecg_analysis)


@visits_bp.route("/<int:visit_id>/edit", methods=["GET", "POST"])
@login_required
@any_role_required
def edit_visit(visit_id):
    """Edit an existing visit."""
    visit_service = VisitService()
    visit = visit_service.get_visit_by_id(visit_id)
    
    form = VisitForm(obj=visit)
    
    # Populate choices for prescriptions (medicaments)
    medicaments = Medicament.query.order_by(Medicament.nom_com).all()
    medicament_choices = [
        (med.num_enr, f"{med.nom_com} ({med.dosage}{med.unite})" if med.dosage and med.unite else med.nom_com)
        for med in medicaments
    ]
    
    for pres_sub in form.prescriptions:
        pres_sub.medicament_num_enr.choices = medicament_choices

    if form.validate_on_submit():
        try:
            # Prepare visit data
            visit_data = {
                'patient_id': form.patient_id.data,
                'visit_date': form.visit_date.data,
                'diagnosis': form.diagnosis.data,
                'follow_up_date': form.follow_up_date.data,
                'payment_total': form.payment_total.data,
                'payment_status': form.payment_status.data,
                'payment_remaining': form.payment_remaining.data,
            }
            
            # Handle ECG file uploads
            if form.ecg_mat.data:
                visit_data['ecg_mat'] = save_uploaded_file(form.ecg_mat.data, 'ecg')
            if form.ecg_hea.data:
                visit_data['ecg_hea'] = save_uploaded_file(form.ecg_hea.data, 'ecg')
            
            # Prepare prescriptions data
            prescriptions_data = []
            for pres_sub in form.prescriptions:
                if pres_sub.medicament_num_enr.data and pres_sub.dosage_instructions.data:
                    prescriptions_data.append({
                        'medicament_num_enr': pres_sub.medicament_num_enr.data,
                        'dosage_instructions': pres_sub.dosage_instructions.data,
                        'quantity': pres_sub.quantity.data,
                    })
            
            # Prepare documents data
            documents_data = []
            for doc_sub in form.documents:
                if doc_sub.file_path.data:
                    file_path = save_uploaded_file(doc_sub.file_path.data, 'docs')
                    if file_path:
                        documents_data.append({
                            'doc_type': doc_sub.doc_type.data,
                            'file_path': file_path,
                            'notes': doc_sub.notes.data,
                        })
            
            # Update visit
            visit_service.update_visit(visit_id, visit_data, prescriptions_data, documents_data)
            
            flash("Visit updated successfully!", "success")
            return redirect(url_for("visits.visit_details", visit_id=visit.id))
            
        except Exception as e:
            flash(f"Error updating visit: {str(e)}", "error")

    return render_template("forms/visit_edit_form.html", form=form, visit=visit)


@visits_bp.route("/<int:visit_id>/analyze_ecg", methods=["POST"])
@login_required
@any_role_required
def analyze_existing_ecg(visit_id):
    """Analyze existing ECG files for a visit that has .mat and .hea files but no ECG prediction data."""
    try:
        visit_service = VisitService()
        predictions = visit_service.analyze_visit_ecg(visit_id)
        
        return jsonify({
            "success": True,
            "message": "ECG analysis completed successfully!",
            "predictions": predictions
        })
        
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Analysis failed: {str(e)}"}), 500

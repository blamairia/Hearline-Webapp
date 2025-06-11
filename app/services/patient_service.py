# app/services/patient_service.py

from sqlalchemy import or_
from app.extensions import db
from app.models.patient import Patient


class PatientService:
    """Service class for patient-related operations."""
    
    @staticmethod
    def create_patient(patient_data):
        """Create a new patient."""
        patient = Patient(**patient_data)
        db.session.add(patient)
        db.session.commit()
        return patient
    
    @staticmethod
    def get_patient_by_id(patient_id):
        """Get patient by ID."""
        return Patient.query.get_or_404(patient_id)
    
    @staticmethod
    def search_patients(query, page=1, per_page=10):
        """Search patients by name."""
        if query:
            pattern = f"%{query}%"
            query_obj = Patient.query.filter(
                or_(
                    Patient.first_name.ilike(pattern),
                    Patient.last_name.ilike(pattern)
                )
            )
        else:
            query_obj = Patient.query
        
        return query_obj.order_by(
            Patient.id.desc(), 
            Patient.first_name, 
            Patient.last_name
        ).paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def update_patient(patient_id, patient_data):
        """Update patient information."""
        patient = Patient.query.get_or_404(patient_id)
        
        for key, value in patient_data.items():
            if hasattr(patient, key):
                setattr(patient, key, value)
        
        db.session.commit()
        return patient
    
    @staticmethod
    def delete_patient(patient_id):
        """Delete a patient."""
        patient = Patient.query.get_or_404(patient_id)
        db.session.delete(patient)
        db.session.commit()
        return True
    
    @staticmethod
    def check_patient_exists(first_name, last_name, exclude_id=None):
        """Check if patient with same name already exists."""
        query = Patient.query.filter(
            db.and_(
                Patient.first_name.ilike(first_name),
                Patient.last_name.ilike(last_name)
            )
        )
        
        if exclude_id:
            query = query.filter(Patient.id != exclude_id)
        
        return query.first() is not None

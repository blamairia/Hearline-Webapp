# app/services/visit_service.py

from app.extensions import db
from app.models.visit import Visit, VisitDocument
from app.models.prescription import Prescription
from app.services.ecg_service import ECGService


class VisitService:
    """Service class for visit-related operations."""
    
    def __init__(self):
        self.ecg_service = ECGService()
    
    @staticmethod
    def create_visit(visit_data, prescriptions_data=None, documents_data=None):
        """Create a new visit with prescriptions and documents."""
        visit = Visit(**visit_data)
        db.session.add(visit)
        db.session.flush()  # Get the visit ID
        
        # Add prescriptions
        if prescriptions_data:
            for pres_data in prescriptions_data:
                if pres_data.get('medicament_num_enr') and pres_data.get('dosage_instructions'):
                    prescription = Prescription(
                        visit_id=visit.id,
                        **pres_data
                    )
                    db.session.add(prescription)
        
        # Add documents
        if documents_data:
            for doc_data in documents_data:
                if doc_data.get('file_path'):
                    document = VisitDocument(
                        visit_id=visit.id,
                        **doc_data
                    )
                    db.session.add(document)
        
        db.session.commit()
        return visit
    
    @staticmethod
    def get_visit_by_id(visit_id):
        """Get visit by ID."""
        return Visit.query.get_or_404(visit_id)
    
    @staticmethod
    def update_visit(visit_id, visit_data, prescriptions_data=None, documents_data=None):
        """Update visit with prescriptions and documents."""
        visit = Visit.query.get_or_404(visit_id)
        
        # Update visit data
        for key, value in visit_data.items():
            if hasattr(visit, key):
                setattr(visit, key, value)
        
        # Update prescriptions
        if prescriptions_data is not None:
            # Remove existing prescriptions
            Prescription.query.filter_by(visit_id=visit_id).delete()
            
            # Add new prescriptions
            for pres_data in prescriptions_data:
                if pres_data.get('medicament_num_enr') and pres_data.get('dosage_instructions'):
                    prescription = Prescription(
                        visit_id=visit_id,
                        **pres_data
                    )
                    db.session.add(prescription)
        
        # Update documents
        if documents_data is not None:
            # Remove existing documents
            VisitDocument.query.filter_by(visit_id=visit_id).delete()
            
            # Add new documents
            for doc_data in documents_data:
                if doc_data.get('file_path'):
                    document = VisitDocument(
                        visit_id=visit_id,
                        **doc_data
                    )
                    db.session.add(document)
        
        db.session.commit()
        return visit
    
    def analyze_visit_ecg(self, visit_id):
        """Analyze ECG files for a visit."""
        visit = self.get_visit_by_id(visit_id)
        
        if not visit.has_ecg_files():
            raise ValueError("Visit does not have ECG files")
        
        try:
            predictions = self.ecg_service.analyze_ecg_files(visit.ecg_mat, visit.ecg_hea)
            visit.ecg_prediction = predictions
            db.session.commit()
            return predictions
        except Exception as e:
            raise Exception(f"ECG analysis failed: {str(e)}")
    
    def get_visit_ecg_waveform(self, visit_id):
        """Get ECG waveform data for a visit."""
        visit = self.get_visit_by_id(visit_id)
        
        if not visit.ecg_hea:
            raise ValueError("Visit does not have ECG HEA file")
        
        return self.ecg_service.get_ecg_waveform_data(visit.ecg_hea)

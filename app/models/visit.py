# app/models/visit.py

from datetime import datetime
from sqlalchemy import JSON
from app.extensions import db


class Visit(db.Model):
    """Visit model for managing patient visits."""
    __tablename__ = "visit"
    
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointment.id"), nullable=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=True)
    visit_date = db.Column(db.DateTime, nullable=False)
    diagnosis = db.Column(db.Text, nullable=True)
    follow_up_date = db.Column(db.DateTime, nullable=True)

    # ECG fields
    ecg_mat = db.Column(db.String(256), nullable=True)   # Path to uploaded .mat
    ecg_hea = db.Column(db.String(256), nullable=True)   # Path to uploaded .hea
    ecg_prediction = db.Column(JSON, nullable=True)      # e.g. {"AF":0.12, ...}

    # Payment fields
    payment_total = db.Column(db.Numeric(10, 2), default=0.00)
    payment_status = db.Column(db.String(20), default="unpaid")  # "paid"/"partial"/"unpaid"
    payment_remaining = db.Column(db.Numeric(10, 2), default=0.00)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    documents = db.relationship("VisitDocument", backref="visit", lazy="dynamic")
    prescriptions = db.relationship("Prescription", backref="visit", lazy="dynamic")
    
    def has_ecg_files(self):
        """Check if visit has ECG files."""
        return self.ecg_mat and self.ecg_hea
    
    def has_ecg_prediction(self):
        """Check if visit has ECG prediction results."""
        return self.ecg_prediction is not None
    
    def get_primary_diagnosis(self):
        """Get primary ECG diagnosis if available."""
        if not self.ecg_prediction:
            return None
        
        class_names = {
            "SNR": "Sinus Rhythm",
            "AF": "Atrial Fibrillation",
            "IAVB": "AV Block",
            "LBBB": "Left Bundle Branch Block",
            "RBBB": "Right Bundle Branch Block",
            "PAC": "Premature Atrial Contraction",
            "PVC": "Premature Ventricular Contraction",
            "STD": "ST Depression",
            "STE": "ST Elevation"
        }
        
        max_prob_abbr = max(self.ecg_prediction, key=self.ecg_prediction.get)
        max_prob_value = self.ecg_prediction[max_prob_abbr]
        
        return {
            "abbreviation": max_prob_abbr,
            "name": class_names.get(max_prob_abbr, max_prob_abbr),
            "probability": max_prob_value
        }
    
    def __repr__(self):
        return f'<Visit {self.id} - {self.patient.get_full_name()} on {self.visit_date}>'


class VisitDocument(db.Model):
    """Document model for managing visit-related documents."""
    __tablename__ = "visit_document"
    
    id = db.Column(db.Integer, primary_key=True)
    visit_id = db.Column(db.Integer, db.ForeignKey("visit.id"), nullable=False)
    doc_type = db.Column(db.String(5), nullable=False)     # e.g. "blood"/"mri"/"xray"
    file_path = db.Column(db.String(256), nullable=False)   # Path to uploaded PDF/image
    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_document_type_display(self):
        """Get human-readable document type."""
        type_mapping = {
            "blood": "Blood Work",
            "mri": "MRI Scan",
            "xray": "X-Ray Scan"
        }
        return type_mapping.get(self.doc_type, self.doc_type.title())
    
    def __repr__(self):
        return f'<VisitDocument {self.id} - {self.doc_type}>'

# app/models/prescription.py

from datetime import datetime
from app.extensions import db


class Medicament(db.Model):
    """Medicament model for managing medication information."""
    __tablename__ = "medicament"  # Already exists in your DB; do not touch data
    
    num_enr = db.Column(db.String(50), primary_key=True)  # key matches your existing table
    nom_com = db.Column(db.String(100), nullable=False)
    nom_dci = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50), nullable=False)
    unite = db.Column(db.String(20), nullable=False)

    # Relationships
    prescriptions = db.relationship("Prescription", backref="medicament", lazy="dynamic")
    
    def get_display_name(self):
        """Get formatted display name for medication."""
        if self.dosage and self.unite:
            return f"{self.nom_com} ({self.dosage}{self.unite})"
        return self.nom_com
    
    def __repr__(self):
        return f'<Medicament {self.nom_com}>'


class Prescription(db.Model):
    """Prescription model for managing visit prescriptions."""
    __tablename__ = "prescription"
    
    id = db.Column(db.Integer, primary_key=True)
    visit_id = db.Column(db.Integer, db.ForeignKey("visit.id"), nullable=False)
    medicament_num_enr = db.Column(db.String(50), db.ForeignKey("medicament.num_enr"), nullable=False)
    dosage_instructions = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Prescription {self.id} - {self.medicament.nom_com}>'

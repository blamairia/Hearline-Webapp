# app/models/appointment.py

from datetime import datetime
from app.extensions import db


class Appointment(db.Model):
    """Appointment model for managing patient appointments."""
    __tablename__ = "appointment"
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)  # scheduled datetime
    reason = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(20), nullable=False, default="scheduled")  # "scheduled"/"completed"/"canceled"
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = db.relationship("Patient", backref="appointments")
    visit = db.relationship("Visit", backref="appointment", uselist=False)
    
    def is_scheduled(self):
        """Check if appointment is scheduled."""
        return self.state == "scheduled"
    
    def is_completed(self):
        """Check if appointment is completed."""
        return self.state == "completed"
    
    def is_canceled(self):
        """Check if appointment is canceled."""
        return self.state == "canceled"
    
    def __repr__(self):
        return f'<Appointment {self.id} - {self.patient.get_full_name()} on {self.date}>'

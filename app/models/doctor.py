# app/models/doctor.py

from datetime import datetime
from app.extensions import db


class Doctor(db.Model):
    """Doctor model for managing doctor information."""
    __tablename__ = "doctor"
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)  # e.g. "Cardiologist"
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    bio = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    appointments = db.relationship("Appointment", backref="doctor", lazy="dynamic")
    visits = db.relationship("Visit", backref="doctor", lazy="dynamic")
    waiting_list = db.relationship("WaitingListEntry", backref="doctor", lazy="dynamic")
    
    def get_full_name(self):
        """Get doctor's full name."""
        return f"Dr. {self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<Doctor {self.first_name} {self.last_name}>'

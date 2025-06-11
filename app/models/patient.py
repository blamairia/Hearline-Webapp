# app/models/patient.py

from datetime import datetime
from app.extensions import db


class Patient(db.Model):
    """Patient model for managing patient information."""
    __tablename__ = "patient"
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)  # "Male"/"Female"/"Other"
    address = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True, unique=True)
    medical_history = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    visits = db.relationship("Visit", backref="patient", lazy="dynamic")
    waiting_list = db.relationship("WaitingListEntry", backref="patient", lazy="dynamic")
    
    def get_full_name(self):
        """Get patient's full name."""
        return f"{self.first_name} {self.last_name}"
    
    def get_age(self):
        """Calculate patient's age."""
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    def __repr__(self):
        return f'<Patient {self.first_name} {self.last_name}>'

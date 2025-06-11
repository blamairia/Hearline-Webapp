# app/models/waiting_list.py

from datetime import datetime
from app.extensions import db


class WaitingListEntry(db.Model):
    """Waiting list entry model for managing patient queue."""
    __tablename__ = "waiting_list_entry"
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    arrival_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(15), nullable=False, default="waiting")  # "waiting"/"called"/"in_progress"/"skipped"
    priority = db.Column(db.SmallInteger, default=5)
    assigned_doctor = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def is_waiting(self):
        """Check if entry is in waiting status."""
        return self.status == "waiting"
    
    def is_called(self):
        """Check if patient has been called."""
        return self.status == "called"
    
    def is_in_progress(self):
        """Check if patient is currently being seen."""
        return self.status == "in_progress"
    
    def __repr__(self):
        return f'<WaitingListEntry {self.id} - {self.patient.get_full_name()}>'

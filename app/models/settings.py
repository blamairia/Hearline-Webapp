# app/models/settings.py

from datetime import datetime
from app.extensions import db


class ClinicInfo(db.Model):
    """Clinic information model for managing clinic details."""
    __tablename__ = "clinic_info"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default="Heartline Medical Clinic")
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    email = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(200), nullable=True)
    operating_hours = db.Column(db.Text, nullable=True)
    specialties = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ClinicInfo {self.name}>'


class GeneralSettings(db.Model):
    """General settings model for managing application settings."""
    __tablename__ = "general_settings"
    
    id = db.Column(db.Integer, primary_key=True)
    default_appointment_duration = db.Column(db.Integer, default=30)  # minutes
    appointment_interval = db.Column(db.Integer, default=15)  # minutes
    weekend_appointments = db.Column(db.Boolean, default=True)
    currency = db.Column(db.String(10), default="DZD")
    date_format = db.Column(db.String(20), default="YYYY-MM-DD")
    auto_backup = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<GeneralSettings {self.id}>'

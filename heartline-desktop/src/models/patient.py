"""
Patient model for Heartline Desktop Application

This module defines the Patient entity with all related fields and relationships.
"""

from sqlalchemy import Column, String, Date, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Patient(Base):
    __tablename__ = 'patient'
    
    # Primary key
    id = Column(Integer, primary_key=True)
    
    # Personal Information (matching web app + enhanced)
    first_name = Column(String(50), nullable=False)  # Match web app length
    last_name = Column(String(50), nullable=False)   # Match web app length
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)      # Match web app: "Male"/"Female"/"Other"
    
    # Contact Information (enhanced)
    phone = Column(String(20), nullable=True)        # Match web app
    email = Column(String(120), nullable=True, unique=True)  # Match web app
    address = Column(Text, nullable=True)            # Match web app
    
    # Medical Information (web app + enhanced)
    medical_history = Column(Text, nullable=True)    # Match web app
    allergies = Column(Text, nullable=True)          # Enhanced field
    current_medications = Column(Text, nullable=True) # Enhanced field
    
    # Insurance Information (enhanced)
    insurance_provider = Column(String(255), nullable=True)
    insurance_number = Column(String(100), nullable=True)
    
    # Emergency Contact (enhanced)
    emergency_contact_name = Column(String(200), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)
    emergency_contact_relationship = Column(String(50), nullable=True)
    
    # Timestamps (match web app)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    appointments = relationship("Appointment", back_populates="patient")
    visits = relationship("Visit", back_populates="patient")
    waiting_list_entries = relationship("WaitingListEntry", back_populates="patient")
    
    @property
    def full_name(self):
        """Get patient's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        """Calculate patient's age"""
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    def __str__(self):
        return f"{self.full_name} ({self.age} years old)"

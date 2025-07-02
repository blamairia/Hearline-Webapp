"""
Complete Database Models for Heartline Desktop Application

This module contains all database models matching the Flask web application structure exactly.
All models inherit directly from Base to match the web app's SQLAlchemy structure.
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime, Boolean, 
    Numeric, SmallInteger, ForeignKey, JSON
)
from sqlalchemy.orm import relationship

from .base import Base

class Patient(Base):
    """Enhanced Patient model with additional desktop fields"""
    
    __tablename__ = "patient"
    
    # Core fields (matching web app)
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)  # e.g. "Male"/"Female"/"Other"
    address = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(120), nullable=True, unique=True)
    medical_history = Column(Text, nullable=True)

    # Enhanced address fields
    city = Column(String(100), nullable=True)
    state = Column(String(50), nullable=True)
    zip_code = Column(String(20), nullable=True)
    country = Column(String(100), nullable=True)

    # Enhanced fields for desktop
    allergies = Column(Text, nullable=True)
    current_medications = Column(Text, nullable=True)
    chronic_conditions = Column(Text, nullable=True)
    family_history = Column(Text, nullable=True)
    
    # Physical information
    height = Column(Integer, nullable=True)  # in cm
    weight = Column(Integer, nullable=True)  # in kg
    blood_type = Column(String(10), nullable=True)
    
    # Additional identification
    ssn = Column(String(20), nullable=True)
    id_number = Column(String(50), nullable=True)
    
    # Insurance information
    insurance_provider = Column(String(255), nullable=True)
    insurance_number = Column(String(100), nullable=True)
    insurance_group = Column(String(100), nullable=True)
    
    # Emergency contact
    emergency_contact_name = Column(String(200), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)
    emergency_contact_relationship = Column(String(50), nullable=True)
    
    # Preferences
    preferred_language = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    visits = relationship("Visit", back_populates="patient", lazy="dynamic")
    waiting_list = relationship("WaitingListEntry", back_populates="patient", lazy="dynamic")
    appointments = relationship("Appointment", back_populates="patient", lazy="dynamic")

    @property
    def full_name(self) -> str:
        """Get patient's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self) -> int:
        """Calculate patient's age"""
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    def __str__(self) -> str:
        return f"Patient(id={self.id}, name='{self.full_name}', age={self.age})"
    
    def __repr__(self) -> str:
        return f"<Patient {self.id}: {self.full_name}>"


class Doctor(Base):
    """Enhanced Doctor model with additional desktop fields"""
    
    __tablename__ = "doctor"
    
    # Core fields (matching web app)
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    specialty = Column(String(100), nullable=False)  # e.g. "Cardiologist"
    phone = Column(String(20), nullable=True)
    email = Column(String(120), nullable=True)
    bio = Column(Text, nullable=True)

    # Enhanced fields for desktop
    office_number = Column(String(50), nullable=True)
    schedule_notes = Column(Text, nullable=True)
    consultation_fee = Column(Numeric(10, 2), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Professional information
    license_number = Column(String(100), nullable=True)
    years_of_experience = Column(Integer, nullable=True)
    education = Column(Text, nullable=True)
    certifications = Column(Text, nullable=True)
    
    # Additional contact
    address = Column(Text, nullable=True)
    emergency_contact = Column(String(200), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    appointments = relationship("Appointment", back_populates="doctor", lazy="dynamic")
    visits = relationship("Visit", back_populates="doctor", lazy="dynamic")
    waiting_list = relationship("WaitingListEntry", back_populates="doctor", lazy="dynamic")
    user = relationship("User", back_populates="doctor", uselist=False)

    @property
    def full_name(self) -> str:
        """Get doctor's full name"""
        return f"Dr. {self.first_name} {self.last_name}"
    
    def __str__(self) -> str:
        return f"Doctor(id={self.id}, name='{self.full_name}', specialty='{self.specialty}')"
    
    def __repr__(self) -> str:
        return f"<Doctor {self.id}: {self.full_name}>"


class Appointment(Base):
    """Enhanced Appointment model with comprehensive fields for desktop application"""
    
    __tablename__ = "appointment"
    
    # Core fields (matching web app)
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)  # scheduled datetime
    reason = Column(String(200), nullable=False)
    state = Column(String(20), nullable=False, default="scheduled")  # appointment status
    patient_id = Column(Integer, ForeignKey("patient.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctor.id"), nullable=True)

    # Enhanced fields for desktop
    appointment_type = Column(String(50), nullable=True, default="consultation")  # "consultation", "follow_up", "emergency", etc.
    duration_minutes = Column(Integer, default=30)  # appointment duration in minutes
    priority = Column(String(20), default="normal")  # "low", "normal", "high", "urgent"
    
    # Notes and communication
    notes = Column(Text, nullable=True)  # internal notes for staff
    patient_notes = Column(Text, nullable=True)  # notes from/for patient
    
    # Status tracking
    confirmed = Column(Boolean, default=False)  # patient confirmation status
    reminder_sent = Column(Boolean, default=False)  # reminder sent status
    
    # Cancellation and rescheduling
    cancelled_reason = Column(String(200), nullable=True)  # reason for cancellation
    cancelled_by = Column(String(50), nullable=True)  # who cancelled (patient/doctor/admin)
    rescheduled_from = Column(Integer, ForeignKey("appointment.id"), nullable=True)  # original appointment if rescheduled

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    visit = relationship("Visit", back_populates="appointment", uselist=False)
    
    # Self-referential relationship for rescheduled appointments
    original_appointment = relationship("Appointment", remote_side=[id], backref="rescheduled_appointments")

    @property
    def full_patient_name(self) -> str:
        """Get patient's full name"""
        if self.patient:
            return f"{self.patient.first_name} {self.patient.last_name}"
        return "Unknown Patient"
    
    @property
    def full_doctor_name(self) -> str:
        """Get doctor's full name"""
        if self.doctor:
            return f"Dr. {self.doctor.first_name} {self.doctor.last_name}"
        return "No Doctor Assigned"
    
    @property
    def appointment_datetime_str(self) -> str:
        """Get formatted appointment date and time"""
        return self.date.strftime("%Y-%m-%d %H:%M") if self.date else ""
    
    @property
    def duration_str(self) -> str:
        """Get formatted duration"""
        return f"{self.duration_minutes} min" if self.duration_minutes else "30 min"
    
    @property
    def status_display(self) -> str:
        """Get display-friendly status"""
        status_map = {
            "scheduled": "Scheduled",
            "confirmed": "Confirmed", 
            "in_progress": "In Progress",
            "completed": "Completed",
            "cancelled": "Cancelled",
            "no_show": "No Show",
            "rescheduled": "Rescheduled",
            "pending": "Pending"
        }
        return status_map.get(self.state, self.state.title())
    
    def __str__(self) -> str:
        return f"Appointment(id={self.id}, patient={self.full_patient_name}, date={self.appointment_datetime_str})"
    
    def __repr__(self) -> str:
        return f"<Appointment {self.id}: {self.full_patient_name} on {self.appointment_datetime_str}>"


class WaitingListEntry(Base):
    """Waiting list entry model matching the web app structure exactly"""
    
    __tablename__ = "waiting_list_entry"
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patient.id"), nullable=False)
    arrival_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String(15), nullable=False, default="waiting")  # "waiting"/"called"/"in_progress"/"skipped"
    priority = Column(SmallInteger, default=5)
    assigned_doctor = Column(Integer, ForeignKey("doctor.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="waiting_list")
    doctor = relationship("Doctor", back_populates="waiting_list", foreign_keys=[assigned_doctor])

    def __str__(self) -> str:
        return f"WaitingListEntry(id={self.id}, patient={self.patient_id}, status={self.status})"
    
    def __repr__(self) -> str:
        return f"<WaitingListEntry {self.id}: {self.status}>"


class Visit(Base):
    """Enhanced Visit model with additional desktop fields"""
    
    __tablename__ = "visit"
    
    # Core fields (matching web app)
    id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer, ForeignKey("appointment.id"), nullable=True)
    patient_id = Column(Integer, ForeignKey("patient.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctor.id"), nullable=True)
    visit_date = Column(DateTime, nullable=False)
    diagnosis = Column(Text, nullable=True)
    follow_up_date = Column(DateTime, nullable=True)

    ecg_mat = Column(String(256), nullable=True)   # Path to uploaded .mat
    ecg_hea = Column(String(256), nullable=True)   # Path to uploaded .hea
    ecg_prediction = Column(JSON, nullable=True)            # e.g. {"AF":0.12, ...}

    payment_total = Column(Numeric(10, 2), default=0.00)
    payment_status = Column(String(20), default="unpaid")  # "paid"/"partial"/"unpaid"
    payment_remaining = Column(Numeric(10, 2), default=0.00)

    # Enhanced fields for desktop
    visit_type = Column(String(50), nullable=True, default="consultation")  # "consultation"/"emergency"/"follow-up"
    visit_duration = Column(Integer, nullable=True)  # minutes
    chief_complaint = Column(Text, nullable=True)
    
    # Vital signs
    blood_pressure = Column(String(20), nullable=True)  # e.g. "120/80"
    heart_rate = Column(Integer, nullable=True)  # bpm
    temperature = Column(Numeric(4, 1), nullable=True)  # celsius
    weight = Column(Numeric(5, 2), nullable=True)  # kg
    height = Column(Numeric(5, 2), nullable=True)  # cm
    oxygen_saturation = Column(Integer, nullable=True)  # percentage
    
    # Clinical notes
    symptoms = Column(Text, nullable=True)
    examination_findings = Column(Text, nullable=True)
    treatment_plan = Column(Text, nullable=True)
    doctor_notes = Column(Text, nullable=True)
    
    # Administrative
    visit_status = Column(String(20), default="completed")  # "scheduled"/"in-progress"/"completed"/"cancelled"
    is_emergency = Column(Boolean, default=False)
    referral_needed = Column(Boolean, default=False)
    referral_to = Column(String(200), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="visits")
    doctor = relationship("Doctor", back_populates="visits")
    appointment = relationship("Appointment", back_populates="visit")
    documents = relationship("VisitDocument", back_populates="visit", lazy="dynamic")
    prescriptions = relationship("Prescription", back_populates="visit", lazy="dynamic")

    def __str__(self) -> str:
        return f"Visit(id={self.id}, patient={self.patient_id}, date={self.visit_date})"
    
    def __repr__(self) -> str:
        return f"<Visit {self.id}: {self.visit_date}>"


class VisitDocument(Base):
    """Visit document model matching the web app structure exactly"""
    
    __tablename__ = "visit_document"
    
    id = Column(Integer, primary_key=True)
    visit_id = Column(Integer, ForeignKey("visit.id"), nullable=False)
    doc_type = Column(String(5), nullable=False)     # e.g. "blood"/"mri"/"xray"
    file_path = Column(String(256), nullable=False)   # Path to uploaded PDF/image
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    visit = relationship("Visit", back_populates="documents")

    def __str__(self) -> str:
        return f"VisitDocument(id={self.id}, visit={self.visit_id}, type={self.doc_type})"
    
    def __repr__(self) -> str:
        return f"<VisitDocument {self.id}: {self.doc_type}>"


class Medicament(Base):
    """Medicament model matching the web app structure exactly"""
    
    __tablename__ = "medicament"  # Already exists in your DB; do not touch data
    
    num_enr = Column(String(50), primary_key=True)  # key matches your existing table
    nom_com = Column(String(100), nullable=False)
    nom_dci = Column(String(100), nullable=False)
    dosage = Column(String(50), nullable=False)
    unite = Column(String(20), nullable=False)

    # Relationships
    prescriptions = relationship("Prescription", back_populates="medicament", lazy="dynamic")

    def __str__(self) -> str:
        return f"Medicament(num_enr={self.num_enr}, nom_com={self.nom_com})"
    
    def __repr__(self) -> str:
        return f"<Medicament {self.num_enr}: {self.nom_com}>"


class Prescription(Base):
    """Prescription model matching the web app structure exactly"""
    
    __tablename__ = "prescription"
    
    id = Column(Integer, primary_key=True)
    visit_id = Column(Integer, ForeignKey("visit.id"), nullable=False)
    medicament_num_enr = Column(String(50), ForeignKey("medicament.num_enr"), nullable=False)
    dosage_instructions = Column(Text, nullable=False)
    quantity = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    visit = relationship("Visit", back_populates="prescriptions")
    medicament = relationship("Medicament", back_populates="prescriptions")

    def __str__(self) -> str:
        return f"Prescription(id={self.id}, visit={self.visit_id}, medicament={self.medicament_num_enr})"
    
    def __repr__(self) -> str:
        return f"<Prescription {self.id}: {self.medicament_num_enr}>"


class ClinicInfo(Base):
    """Clinic info model matching the web app structure exactly"""
    
    __tablename__ = "clinic_info"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, default="Heartline Medical Clinic")
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    email = Column(String(120), nullable=True)
    website = Column(String(200), nullable=True)
    operating_hours = Column(Text, nullable=True)
    specialties = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __str__(self) -> str:
        return f"ClinicInfo(id={self.id}, name={self.name})"
    
    def __repr__(self) -> str:
        return f"<ClinicInfo {self.id}: {self.name}>"


class GeneralSettings(Base):
    """General settings model matching the web app structure exactly"""
    
    __tablename__ = "general_settings"
    
    id = Column(Integer, primary_key=True)
    default_appointment_duration = Column(Integer, default=30)  # minutes
    appointment_interval = Column(Integer, default=15)  # minutes
    weekend_appointments = Column(Boolean, default=True)
    currency = Column(String(10), default="DZD")
    date_format = Column(String(20), default="YYYY-MM-DD")
    auto_backup = Column(Boolean, default=True)
    default_doctor_id = Column(Integer, ForeignKey("doctor.id"), nullable=True)  # Default doctor for appointments
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __str__(self) -> str:
        return f"GeneralSettings(id={self.id}, currency={self.currency})"
    
    def __repr__(self) -> str:
        return f"<GeneralSettings {self.id}>"


class User(Base):
    """User model for authentication with role-based access control"""
    
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(String(20), nullable=False, default='assistant')  # 'doctor' or 'assistant'
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Optional reference to doctor record (only for doctor users)
    doctor_id = Column(Integer, ForeignKey("doctor.id"), nullable=True)
    
    # Additional profile information
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    doctor = relationship("Doctor", back_populates="user")
    sessions = relationship("UserSession", back_populates="user", lazy="dynamic")

    @property
    def full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def has_role(self, role: str) -> bool:
        """Check if user has specific role"""
        return self.role == role
    
    def is_doctor(self) -> bool:
        """Check if user is a doctor"""
        return self.role == 'doctor'
    
    def is_assistant(self) -> bool:
        """Check if user is an assistant"""
        return self.role == 'assistant'

    def __str__(self) -> str:
        return f"User(id={self.id}, username={self.username}, role={self.role})"
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"


class UserSession(Base):
    """Model to track user sessions for better security"""
    
    __tablename__ = "user_session"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    session_token = Column(String(255), unique=True, nullable=False)
    ip_address = Column(String(45), nullable=True)  # IPv6 support
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    
    def is_expired(self) -> bool:
        """Check if session is expired"""
        return datetime.utcnow() > self.expires_at
    
    def __str__(self) -> str:
        return f"UserSession(id={self.id}, user={self.user_id}, active={self.is_active})"
    
    def __repr__(self) -> str:
        return f"<UserSession {self.session_token}>"

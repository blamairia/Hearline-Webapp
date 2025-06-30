"""
Doctor Dialog for Creating and Editing Doctors

This dialog provides a comprehensive form for creating new doctors or editing existing ones.
Includes all database fields with responsive design and proper spacing.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLineEdit, QTextEdit, QComboBox, QLabel,
    QFrame, QMessageBox, QGroupBox, QSpinBox, QDoubleSpinBox,
    QScrollArea, QWidget, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import Optional
from datetime import datetime

from src.models.complete_models import Doctor
from src.core.database import db_manager
from src.ui.styles import AppColors, AppStyles


class DoctorDialog(QDialog):
    """Dialog for creating or editing a doctor with all database fields"""
    
    doctor_saved = pyqtSignal(int)  # Emitted when doctor is saved
    
    def __init__(self, doctor_id: Optional[int] = None, parent=None):
        super().__init__(parent)
        
        # Validate doctor_id
        if doctor_id is not None:
            if not isinstance(doctor_id, int) or doctor_id <= 0:
                raise ValueError(f"Invalid doctor_id: {doctor_id} (type: {type(doctor_id)})")
        
        self.doctor_id = doctor_id
        self.doctor_data = None  # Store extracted data
        self.is_editing = doctor_id is not None
        
        self.setWindowTitle("Edit Doctor" if self.is_editing else "New Doctor")
        self.setMinimumSize(700, 600)
        self.resize(700, 700)
        self.setModal(True)
        
        # Apply styles
        self.setStyleSheet(AppStyles.DIALOG_STYLE)
        
        self.setup_ui()
        self.setup_connections()
        
        if self.is_editing:
            self.load_doctor()
    
    def setup_ui(self):
        """Setup the user interface with responsive design"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("👨‍⚕️ " + ("Edit Doctor" if self.is_editing else "Add New Doctor"))
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {AppColors.PRIMARY}; margin: 10px 0px;")
        layout.addWidget(title_label)
        
        # Create tabs for organized input
        self.tab_widget = QTabWidget()
        
        # Basic Information Tab
        self.basic_tab = self.create_basic_info_tab()
        self.tab_widget.addTab(self.basic_tab, "📋 Basic Info")
        
        # Professional Information Tab
        self.professional_tab = self.create_professional_info_tab()
        self.tab_widget.addTab(self.professional_tab, "🏥 Professional")
        
        # Contact & Additional Tab
        self.contact_tab = self.create_contact_info_tab()
        self.tab_widget.addTab(self.contact_tab, "📞 Contact & More")
        
        layout.addWidget(self.tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        if self.is_editing:
            self.delete_btn = QPushButton("🗑️ Delete Doctor")
            self.delete_btn.setStyleSheet(AppStyles.DANGER_BUTTON_STYLE)
            self.delete_btn.setMinimumHeight(35)
            button_layout.addWidget(self.delete_btn)
        
        button_layout.addStretch()
        
        self.cancel_btn = QPushButton("❌ Cancel")
        self.cancel_btn.setStyleSheet(AppStyles.SECONDARY_BUTTON_STYLE)
        self.cancel_btn.setMinimumHeight(35)
        
        self.save_btn = QPushButton("💾 Save Doctor")
        self.save_btn.setStyleSheet(AppStyles.PRIMARY_BUTTON_STYLE)
        self.save_btn.setMinimumHeight(35)
        
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.save_btn)
        
        layout.addLayout(button_layout)
    
    def create_basic_info_tab(self) -> QWidget:
        """Create the basic information tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # Personal Information Group
        personal_group = QGroupBox("Personal Information")
        personal_layout = QFormLayout(personal_group)
        personal_layout.setSpacing(10)
        
        self.first_name_edit = QLineEdit()
        self.first_name_edit.setPlaceholderText("Enter first name")
        self.first_name_edit.setMinimumHeight(35)
        personal_layout.addRow("*First Name:", self.first_name_edit)
        
        self.last_name_edit = QLineEdit()
        self.last_name_edit.setPlaceholderText("Enter last name")
        self.last_name_edit.setMinimumHeight(35)
        personal_layout.addRow("*Last Name:", self.last_name_edit)
        
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("doctor@hospital.com")
        self.email_edit.setMinimumHeight(35)
        personal_layout.addRow("Email:", self.email_edit)
        
        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("(XXX) XXX-XXXX")
        self.phone_edit.setMinimumHeight(35)
        personal_layout.addRow("Phone:", self.phone_edit)
        
        layout.addWidget(personal_group)
        
        # Basic Professional Info
        basic_prof_group = QGroupBox("Basic Professional Information")
        basic_prof_layout = QFormLayout(basic_prof_group)
        basic_prof_layout.setSpacing(10)
        
        self.specialty_edit = QLineEdit()
        self.specialty_edit.setPlaceholderText("e.g., Cardiology, Dermatology")
        self.specialty_edit.setMinimumHeight(35)
        basic_prof_layout.addRow("*Specialty:", self.specialty_edit)
        
        self.office_number_edit = QLineEdit()
        self.office_number_edit.setPlaceholderText("Office/Room number")
        self.office_number_edit.setMinimumHeight(35)
        basic_prof_layout.addRow("Office Number:", self.office_number_edit)
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Active", "Inactive", "On Leave"])
        self.status_combo.setMinimumHeight(35)
        basic_prof_layout.addRow("Status:", self.status_combo)
        
        layout.addWidget(basic_prof_group)
        layout.addStretch()
        
        return widget
    
    def create_professional_info_tab(self) -> QWidget:
        """Create the professional information tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # Credentials Group
        credentials_group = QGroupBox("Professional Credentials")
        credentials_layout = QFormLayout(credentials_group)
        credentials_layout.setSpacing(10)
        
        self.license_edit = QLineEdit()
        self.license_edit.setPlaceholderText("Medical license number")
        self.license_edit.setMinimumHeight(35)
        credentials_layout.addRow("License Number:", self.license_edit)
        
        self.experience_spin = QSpinBox()
        self.experience_spin.setRange(0, 50)
        self.experience_spin.setSuffix(" years")
        self.experience_spin.setMinimumHeight(35)
        credentials_layout.addRow("Years of Experience:", self.experience_spin)
        
        self.consultation_fee_spin = QDoubleSpinBox()
        self.consultation_fee_spin.setRange(0, 10000)
        self.consultation_fee_spin.setPrefix("$")
        self.consultation_fee_spin.setValue(100.00)
        self.consultation_fee_spin.setMinimumHeight(35)
        credentials_layout.addRow("Consultation Fee:", self.consultation_fee_spin)
        
        layout.addWidget(credentials_group)
        
        # Education & Certifications Group
        education_group = QGroupBox("Education & Certifications")
        education_layout = QFormLayout(education_group)
        education_layout.setSpacing(10)
        
        self.education_edit = QTextEdit()
        self.education_edit.setPlaceholderText("Educational background, degrees, institutions...")
        self.education_edit.setMinimumHeight(80)
        self.education_edit.setMaximumHeight(120)
        education_layout.addRow("Education:", self.education_edit)
        
        self.certifications_edit = QTextEdit()
        self.certifications_edit.setPlaceholderText("Professional certifications, board certifications...")
        self.certifications_edit.setMinimumHeight(80)
        self.certifications_edit.setMaximumHeight(120)
        education_layout.addRow("Certifications:", self.certifications_edit)
        
        layout.addWidget(education_group)
        layout.addStretch()
        
        return widget
    
    def create_contact_info_tab(self) -> QWidget:
        """Create the contact and additional information tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # Contact Information Group
        contact_group = QGroupBox("Contact Information")
        contact_layout = QFormLayout(contact_group)
        contact_layout.setSpacing(10)
        
        self.address_edit = QTextEdit()
        self.address_edit.setPlaceholderText("Full address...")
        self.address_edit.setMinimumHeight(60)
        self.address_edit.setMaximumHeight(80)
        contact_layout.addRow("Address:", self.address_edit)
        
        self.emergency_contact_edit = QLineEdit()
        self.emergency_contact_edit.setPlaceholderText("Emergency contact information")
        self.emergency_contact_edit.setMinimumHeight(35)
        contact_layout.addRow("Emergency Contact:", self.emergency_contact_edit)
        
        layout.addWidget(contact_group)
        
        # Additional Information Group
        additional_group = QGroupBox("Additional Information")
        additional_layout = QFormLayout(additional_group)
        additional_layout.setSpacing(10)
        
        self.bio_edit = QTextEdit()
        self.bio_edit.setPlaceholderText("Professional biography, specializations, achievements...")
        self.bio_edit.setMinimumHeight(80)
        self.bio_edit.setMaximumHeight(120)
        additional_layout.addRow("Biography:", self.bio_edit)
        
        self.schedule_notes_edit = QTextEdit()
        self.schedule_notes_edit.setPlaceholderText("Schedule notes, availability, special instructions...")
        self.schedule_notes_edit.setMinimumHeight(60)
        self.schedule_notes_edit.setMaximumHeight(80)
        additional_layout.addRow("Schedule Notes:", self.schedule_notes_edit)
        
        layout.addWidget(additional_group)
        layout.addStretch()
        
        return widget
    
    def setup_connections(self):
        """Setup signal connections"""
        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self.save_doctor)
        
        if self.is_editing:
            self.delete_btn.clicked.connect(self.delete_doctor)
    
    def load_doctor(self):
        """Load doctor data for editing"""
        try:
            print(f"Loading doctor with ID: {self.doctor_id} (type: {type(self.doctor_id)})")  # Debug
            
            with db_manager.get_session() as session:
                doctor = session.query(Doctor).filter(Doctor.id == self.doctor_id).first()
                if not doctor:
                    QMessageBox.critical(self, "Error", "Doctor not found!")
                    self.reject()
                    return
                
                # Extract all data before session closes
                self.doctor_data = {
                    'id': doctor.id,
                    'first_name': doctor.first_name,
                    'last_name': doctor.last_name,
                    'email': doctor.email,
                    'phone': doctor.phone,
                    'specialty': doctor.specialty,
                    'office_number': doctor.office_number,
                    'license_number': doctor.license_number,
                    'years_of_experience': doctor.years_of_experience,
                    'consultation_fee': doctor.consultation_fee,
                    'is_active': doctor.is_active,
                    'education': doctor.education,
                    'certifications': doctor.certifications,
                    'address': doctor.address,
                    'emergency_contact': doctor.emergency_contact,
                    'bio': doctor.bio,
                    'schedule_notes': doctor.schedule_notes,
                }
                
                # Populate form fields
                self.first_name_edit.setText(self.doctor_data['first_name'] or "")
                self.last_name_edit.setText(self.doctor_data['last_name'] or "")
                self.email_edit.setText(self.doctor_data['email'] or "")
                self.phone_edit.setText(self.doctor_data['phone'] or "")
                self.specialty_edit.setText(self.doctor_data['specialty'] or "")
                self.office_number_edit.setText(self.doctor_data['office_number'] or "")
                self.license_edit.setText(self.doctor_data['license_number'] or "")
                
                if self.doctor_data['years_of_experience']:
                    self.experience_spin.setValue(self.doctor_data['years_of_experience'])
                if self.doctor_data['consultation_fee']:
                    self.consultation_fee_spin.setValue(float(self.doctor_data['consultation_fee']))
                
                # Set status
                if self.doctor_data['is_active']:
                    self.status_combo.setCurrentText("Active")
                else:
                    self.status_combo.setCurrentText("Inactive")
                
                # Set text areas
                self.education_edit.setPlainText(self.doctor_data['education'] or "")
                self.certifications_edit.setPlainText(self.doctor_data['certifications'] or "")
                self.address_edit.setPlainText(self.doctor_data['address'] or "")
                self.emergency_contact_edit.setText(self.doctor_data['emergency_contact'] or "")
                self.bio_edit.setPlainText(self.doctor_data['bio'] or "")
                self.schedule_notes_edit.setPlainText(self.doctor_data['schedule_notes'] or "")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load doctor:\n{str(e)}")
            self.reject()
    
    def validate_form(self) -> bool:
        """Validate form inputs"""
        if not self.first_name_edit.text().strip():
            QMessageBox.warning(self, "Validation Error", "First name is required!")
            self.first_name_edit.setFocus()
            return False
        
        if not self.last_name_edit.text().strip():
            QMessageBox.warning(self, "Validation Error", "Last name is required!")
            self.last_name_edit.setFocus()
            return False
        
        if not self.specialty_edit.text().strip():
            QMessageBox.warning(self, "Validation Error", "Specialty is required!")
            self.specialty_edit.setFocus()
            return False
        
        # Validate email format if provided
        email = self.email_edit.text().strip()
        if email and "@" not in email:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid email address!")
            self.email_edit.setFocus()
            return False
        
        return True
    
    def save_doctor(self):
        """Save doctor data"""
        if not self.validate_form():
            return
        
        try:
            with db_manager.get_session() as session:
                if self.is_editing:
                    doctor = session.query(Doctor).filter(Doctor.id == self.doctor_id).first()
                    if not doctor:
                        QMessageBox.critical(self, "Error", "Doctor not found!")
                        return
                else:
                    doctor = Doctor()
                    session.add(doctor)
                
                # Update doctor data with all fields
                doctor.first_name = self.first_name_edit.text().strip()
                doctor.last_name = self.last_name_edit.text().strip()
                doctor.email = self.email_edit.text().strip() or None
                doctor.phone = self.phone_edit.text().strip() or None
                doctor.specialty = self.specialty_edit.text().strip()
                doctor.office_number = self.office_number_edit.text().strip() or None
                doctor.license_number = self.license_edit.text().strip() or None
                doctor.years_of_experience = self.experience_spin.value() if self.experience_spin.value() > 0 else None
                doctor.consultation_fee = self.consultation_fee_spin.value()
                doctor.is_active = self.status_combo.currentText() == "Active"
                doctor.education = self.education_edit.toPlainText().strip() or None
                doctor.certifications = self.certifications_edit.toPlainText().strip() or None
                doctor.address = self.address_edit.toPlainText().strip() or None
                doctor.emergency_contact = self.emergency_contact_edit.text().strip() or None
                doctor.bio = self.bio_edit.toPlainText().strip() or None
                doctor.schedule_notes = self.schedule_notes_edit.toPlainText().strip() or None
                
                if not self.is_editing:
                    doctor.created_at = datetime.now()
                else:
                    doctor.updated_at = datetime.now()
                
                session.commit()
                
                # Get the doctor ID for the signal
                doctor_id = doctor.id
                
            self.doctor_saved.emit(doctor_id)
            
            action = "updated" if self.is_editing else "created"
            QMessageBox.information(self, "Success", f"Doctor {action} successfully!")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save doctor:\n{str(e)}")
    
    def delete_doctor(self):
        """Delete the current doctor"""
        if not self.doctor_data:
            QMessageBox.warning(self, "Error", "No doctor data available!")
            return
            
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete Dr. {self.doctor_data['first_name']} {self.doctor_data['last_name']}?\n\n"
            "This action cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                with db_manager.get_session() as session:
                    doctor = session.query(Doctor).filter(Doctor.id == self.doctor_id).first()
                    if doctor:
                        session.delete(doctor)
                        session.commit()
                
                QMessageBox.information(self, "Success", "Doctor deleted successfully!")
                self.doctor_saved.emit(self.doctor_id)  # Signal refresh
                self.accept()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete doctor:\n{str(e)}")

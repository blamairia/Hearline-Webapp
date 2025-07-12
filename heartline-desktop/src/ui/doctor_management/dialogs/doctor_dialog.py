"""
Doctor Dialog for Creating and Editing Doctors

Simple dialog for doctor CRUD operations without complex features.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLineEdit, QTextEdit, QComboBox, QSpinBox, QLabel,
    QMessageBox, QGroupBox, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import Optional
from datetime import datetime

from src.models.complete_models import Doctor
from src.core.database import db_manager
from src.ui.styles import AppColors, AppStyles


class DoctorDialog(QDialog):
    """Simple dialog for creating or editing a doctor"""
    
    doctor_saved = pyqtSignal(int)  # Emitted when doctor is saved
    
    def __init__(self, doctor_id: Optional[int] = None, parent=None):
        super().__init__(parent)
        self.doctor_id = doctor_id
        self.doctor = None
        self.is_editing = doctor_id is not None
        
        self.setWindowTitle("Edit Doctor" if self.is_editing else "New Doctor")
        self.setFixedSize(600, 500)
        self.setModal(True)
        
        # Apply styles
        self.setStyleSheet(AppStyles.DIALOG_STYLE)
        
        self.setup_ui()
        self.setup_connections()
        
        if self.is_editing:
            self.load_doctor()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("👨‍⚕️ " + ("Edit Doctor" if self.is_editing else "Add New Doctor"))
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {AppColors.PRIMARY}; margin: 10px;")
        layout.addWidget(title_label)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Basic Information Group
        basic_group = QGroupBox("Basic Information")
        basic_layout = QFormLayout(basic_group)
        
        self.first_name_edit = QLineEdit()
        self.first_name_edit.setPlaceholderText("Enter first name")
        basic_layout.addRow("*First Name:", self.first_name_edit)
        
        self.last_name_edit = QLineEdit()
        self.last_name_edit.setPlaceholderText("Enter last name")
        basic_layout.addRow("*Last Name:", self.last_name_edit)
        
        self.specialty_edit = QLineEdit()
        self.specialty_edit.setPlaceholderText("e.g., Cardiology, Neurology")
        basic_layout.addRow("*Specialty:", self.specialty_edit)
        
        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("(XXX) XXX-XXXX")
        basic_layout.addRow("Phone:", self.phone_edit)
        
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("doctor@email.com")
        basic_layout.addRow("Email:", self.email_edit)
        
        layout.addWidget(basic_group)
        
        # Professional Information Group
        prof_group = QGroupBox("Professional Information")
        prof_layout = QFormLayout(prof_group)
        
        self.license_number_edit = QLineEdit()
        self.license_number_edit.setPlaceholderText("Medical license number")
        prof_layout.addRow("License Number:", self.license_number_edit)
        
        self.years_experience_spin = QSpinBox()
        self.years_experience_spin.setRange(0, 50)
        self.years_experience_spin.setSuffix(" years")
        prof_layout.addRow("Experience:", self.years_experience_spin)
        
        self.consultation_fee_spin = QSpinBox()
        self.consultation_fee_spin.setRange(0, 10000)
        self.consultation_fee_spin.setSuffix(" $")
        prof_layout.addRow("Consultation Fee:", self.consultation_fee_spin)
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Active", "Inactive", "On Leave"])
        prof_layout.addRow("Status:", self.status_combo)
        
        layout.addWidget(prof_group)
        
        # Additional Information Group
        additional_group = QGroupBox("Additional Information")
        additional_layout = QFormLayout(additional_group)
        
        self.qualifications_edit = QTextEdit()
        self.qualifications_edit.setPlaceholderText("List qualifications, certifications...")
        self.qualifications_edit.setMaximumHeight(80)
        additional_layout.addRow("Qualifications:", self.qualifications_edit)
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Additional notes...")
        self.notes_edit.setMaximumHeight(60)
        additional_layout.addRow("Notes:", self.notes_edit)
        
        layout.addWidget(additional_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.cancel_btn = QPushButton("❌ Cancel")
        self.save_btn = QPushButton("💾 Save Doctor")
        
        if self.is_editing:
            self.delete_btn = QPushButton("🗑️ Delete")
            self.delete_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; }")
            button_layout.addWidget(self.delete_btn)
        
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.save_btn)
        
        layout.addLayout(button_layout)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self.save_doctor)
        
        if self.is_editing:
            self.delete_btn.clicked.connect(self.delete_doctor)
    
    def load_doctor(self):
        """Load doctor data for editing"""
        try:
            with db_manager.get_session() as session:
                doctor = session.query(Doctor).filter(Doctor.id == self.doctor_id).first()
                if not doctor:
                    QMessageBox.critical(self, "Error", "Doctor not found!")
                    self.reject()
                    return
                
                # Extract data before session closes
                self.doctor = doctor
                
                # Populate form fields
                self.first_name_edit.setText(doctor.first_name or "")
                self.last_name_edit.setText(doctor.last_name or "")
                self.specialty_edit.setText(doctor.specialty or "")
                self.phone_edit.setText(doctor.phone or "")
                self.email_edit.setText(doctor.email or "")
                self.license_number_edit.setText(doctor.license_number or "")
                
                if doctor.years_experience:
                    self.years_experience_spin.setValue(doctor.years_experience)
                if doctor.consultation_fee:
                    self.consultation_fee_spin.setValue(int(doctor.consultation_fee))
                
                if doctor.status:
                    index = self.status_combo.findText(doctor.status)
                    if index >= 0:
                        self.status_combo.setCurrentIndex(index)
                
                self.qualifications_edit.setPlainText(doctor.qualifications or "")
                self.notes_edit.setPlainText(doctor.notes or "")
                
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
                
                # Update doctor data
                doctor.first_name = self.first_name_edit.text().strip()
                doctor.last_name = self.last_name_edit.text().strip()
                doctor.specialty = self.specialty_edit.text().strip()
                doctor.phone = self.phone_edit.text().strip() or None
                doctor.email = self.email_edit.text().strip() or None
                doctor.license_number = self.license_number_edit.text().strip() or None
                doctor.years_experience = self.years_experience_spin.value()
                doctor.consultation_fee = float(self.consultation_fee_spin.value())
                doctor.status = self.status_combo.currentText()
                doctor.qualifications = self.qualifications_edit.toPlainText().strip() or None
                doctor.notes = self.notes_edit.toPlainText().strip() or None
                
                if not self.is_editing:
                    doctor.created_at = datetime.now()
                
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
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete doctor {self.doctor.first_name} {self.doctor.last_name}?\n\n"
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

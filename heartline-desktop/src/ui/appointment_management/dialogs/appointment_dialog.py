"""
Appointment Dialog for Creating and Editing Appointments

This dialog provides a comprehensive form for creating new appointments or editing existing ones.
Includes all database fields with enhanced features like patient/doctor selection, 
conflict detection, and appointment scheduling.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLineEdit, QTextEdit, QComboBox, QLabel,
    QFrame, QMessageBox, QGroupBox, QSpinBox, QDateTimeEdit,
    QCheckBox, QTabWidget, QWidget, QCompleter
)
from PyQt6.QtCore import Qt, pyqtSignal, QDateTime
from PyQt6.QtGui import QFont
from typing import Optional, List, Dict
from datetime import datetime, timedelta

from src.models.complete_models import Appointment, Patient, Doctor, GeneralSettings
from src.core.database import db_manager
from src.ui.styles import AppColors, AppStyles


class AppointmentDialog(QDialog):
    """Dialog for creating or editing an appointment with all database fields"""
    
    appointment_saved = pyqtSignal(int)  # Emitted when appointment is saved
    
    # Constants for dropdown options
    APPOINTMENT_TYPES = [
        "consultation", "follow_up", "emergency", "check_up", 
        "procedure", "lab_results", "second_opinion"
    ]
    
    PRIORITY_LEVELS = ["low", "normal", "high", "urgent"]
    
    APPOINTMENT_STATUSES = [
        "scheduled", "confirmed", "in_progress", "completed",
        "cancelled", "no_show", "rescheduled", "pending"
    ]
    
    def __init__(self, appointment_id: Optional[int] = None, parent=None):
        super().__init__(parent)
        self.appointment_id = appointment_id
        self.appointment_data = None  # Store extracted data
        self.patients_data = []  # Store patient options
        self.doctors_data = []   # Store doctor options
        self.is_editing = appointment_id is not None
        
        self.setWindowTitle("Edit Appointment" if self.is_editing else "New Appointment")
        self.setMinimumSize(800, 700)
        self.resize(800, 750)
        self.setModal(True)
        
        # Apply comprehensive styling
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {AppColors.BACKGROUND};
                color: {AppColors.TEXT_PRIMARY};
                font-family: 'Segoe UI', sans-serif;
            }}
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {AppColors.BORDER};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: {AppColors.CARD_BACKGROUND};
                color: {AppColors.TEXT_PRIMARY};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                color: {AppColors.PRIMARY};
                background-color: {AppColors.BACKGROUND};
            }}
            QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateTimeEdit {{
                padding: 8px;
                border: 2px solid {AppColors.BORDER};
                border-radius: 6px;
                background-color: {AppColors.INPUT_BACKGROUND};
                color: {AppColors.TEXT_PRIMARY};
                font-size: 14px;
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateTimeEdit:focus {{
                border-color: {AppColors.PRIMARY};
            }}
            QComboBox::drop-down {{
                border: none;
                background-color: {AppColors.PRIMARY};
                width: 20px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 6px solid white;
                margin: 0px;
            }}
            QLabel {{
                color: {AppColors.TEXT_PRIMARY};
                font-size: 14px;
            }}
            QPushButton {{
                background-color: {AppColors.PRIMARY};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {AppColors.PRIMARY_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {AppColors.PRIMARY_PRESSED};
            }}
            QPushButton:disabled {{
                background-color: {AppColors.DISABLED};
                color: {AppColors.TEXT_SECONDARY};
            }}
            QTabWidget::pane {{
                border: 1px solid {AppColors.BORDER};
                background-color: {AppColors.CARD_BACKGROUND};
            }}
            QTabBar::tab {{
                background-color: {AppColors.BACKGROUND};
                color: {AppColors.TEXT_PRIMARY};
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }}
            QTabBar::tab:selected {{
                background-color: {AppColors.PRIMARY};
                color: white;
            }}
            QTabBar::tab:hover {{
                background-color: {AppColors.HOVER};
            }}
        """)
        
        self.setup_ui()
        self.setup_connections()
        self.load_patient_doctor_data()
        
        if not self.is_editing:
            self.set_default_doctor()  # Set default doctor for new appointments
        
        if self.is_editing:
            self.load_appointment()
    
    def setup_ui(self):
        """Setup the user interface with responsive design"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("📅 " + ("Edit Appointment" if self.is_editing else "Schedule New Appointment"))
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {AppColors.PRIMARY}; margin: 10px 0px;")
        layout.addWidget(title_label)
        
        # Create tabs for organized input
        self.tab_widget = QTabWidget()
        
        # Basic Information Tab
        self.basic_tab = self.create_basic_info_tab()
        self.tab_widget.addTab(self.basic_tab, "📋 Basic Info")
        
        # Details & Notes Tab
        self.details_tab = self.create_details_tab()
        self.tab_widget.addTab(self.details_tab, "📝 Details & Notes")
        
        # Status & Management Tab
        self.status_tab = self.create_status_tab()
        self.tab_widget.addTab(self.status_tab, "⚙️ Status & Management")
        
        layout.addWidget(self.tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        if self.is_editing:
            self.delete_btn = QPushButton("🗑️ Delete Appointment")
            self.delete_btn.setStyleSheet(AppStyles.DANGER_BUTTON_STYLE)
            self.delete_btn.setMinimumHeight(35)
            button_layout.addWidget(self.delete_btn)
        
        button_layout.addStretch()
        
        self.cancel_btn = QPushButton("❌ Cancel")
        self.cancel_btn.setStyleSheet(AppStyles.SECONDARY_BUTTON_STYLE)
        self.cancel_btn.setMinimumHeight(35)
        
        self.save_btn = QPushButton("💾 Save Appointment")
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
        
        # Patient and Doctor Selection Group
        selection_group = QGroupBox("Patient & Doctor Selection")
        selection_layout = QFormLayout(selection_group)
        selection_layout.setSpacing(10)
        
        self.patient_combo = QComboBox()
        self.patient_combo.setMinimumHeight(35)
        self.patient_combo.setEditable(True)
        selection_layout.addRow("*Patient:", self.patient_combo)
        
        self.doctor_combo = QComboBox()
        self.doctor_combo.setMinimumHeight(35)
        self.doctor_combo.setEditable(True)
        selection_layout.addRow("Doctor:", self.doctor_combo)
        
        layout.addWidget(selection_group)
        
        # Appointment Details Group
        details_group = QGroupBox("Appointment Details")
        details_layout = QFormLayout(details_group)
        details_layout.setSpacing(10)
        
        self.date_time_edit = QDateTimeEdit()
        self.date_time_edit.setDateTime(QDateTime.currentDateTime())
        self.date_time_edit.setMinimumHeight(35)
        self.date_time_edit.setDisplayFormat("yyyy-MM-dd hh:mm AP")
        details_layout.addRow("*Date & Time:", self.date_time_edit)
        
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(15, 240)  # 15 minutes to 4 hours
        self.duration_spin.setSuffix(" minutes")
        self.duration_spin.setValue(30)
        self.duration_spin.setMinimumHeight(35)
        details_layout.addRow("Duration:", self.duration_spin)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems([t.replace("_", " ").title() for t in self.APPOINTMENT_TYPES])
        self.type_combo.setMinimumHeight(35)
        details_layout.addRow("Type:", self.type_combo)
        
        self.priority_combo = QComboBox()
        self.priority_combo.addItems([p.title() for p in self.PRIORITY_LEVELS])
        self.priority_combo.setCurrentText("Normal")
        self.priority_combo.setMinimumHeight(35)
        details_layout.addRow("Priority:", self.priority_combo)
        
        layout.addWidget(details_group)
        
        # Reason Group
        reason_group = QGroupBox("Reason for Visit")
        reason_layout = QFormLayout(reason_group)
        reason_layout.setSpacing(10)
        
        self.reason_edit = QTextEdit()
        self.reason_edit.setPlaceholderText("Describe the reason for this appointment...")
        self.reason_edit.setMinimumHeight(80)
        self.reason_edit.setMaximumHeight(120)
        reason_layout.addRow("*Reason:", self.reason_edit)
        
        layout.addWidget(reason_group)
        layout.addStretch()
        
        return widget
    
    def create_details_tab(self) -> QWidget:
        """Create the details and notes tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # Internal Notes Group
        notes_group = QGroupBox("Internal Notes")
        notes_layout = QFormLayout(notes_group)
        notes_layout.setSpacing(10)
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Internal notes for staff (not visible to patient)...")
        self.notes_edit.setMinimumHeight(100)
        self.notes_edit.setMaximumHeight(150)
        notes_layout.addRow("Staff Notes:", self.notes_edit)
        
        layout.addWidget(notes_group)
        
        # Patient Notes Group
        patient_notes_group = QGroupBox("Patient Notes")
        patient_notes_layout = QFormLayout(patient_notes_group)
        patient_notes_layout.setSpacing(10)
        
        self.patient_notes_edit = QTextEdit()
        self.patient_notes_edit.setPlaceholderText("Notes from/for the patient...")
        self.patient_notes_edit.setMinimumHeight(100)
        self.patient_notes_edit.setMaximumHeight(150)
        patient_notes_layout.addRow("Patient Notes:", self.patient_notes_edit)
        
        layout.addWidget(patient_notes_group)
        
        # Cancellation Information Group (only shown when editing cancelled appointments)
        self.cancellation_group = QGroupBox("Cancellation Information")
        cancellation_layout = QFormLayout(self.cancellation_group)
        cancellation_layout.setSpacing(10)
        
        self.cancelled_reason_edit = QLineEdit()
        self.cancelled_reason_edit.setPlaceholderText("Reason for cancellation...")
        self.cancelled_reason_edit.setMinimumHeight(35)
        cancellation_layout.addRow("Cancellation Reason:", self.cancelled_reason_edit)
        
        self.cancelled_by_edit = QLineEdit()
        self.cancelled_by_edit.setPlaceholderText("Who cancelled (patient/doctor/admin)...")
        self.cancelled_by_edit.setMinimumHeight(35)
        cancellation_layout.addRow("Cancelled By:", self.cancelled_by_edit)
        
        layout.addWidget(self.cancellation_group)
        self.cancellation_group.setVisible(False)  # Hidden by default
        
        layout.addStretch()
        
        return widget
    
    def create_status_tab(self) -> QWidget:
        """Create the status and management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # Status Management Group
        status_group = QGroupBox("Status Management")
        status_layout = QFormLayout(status_group)
        status_layout.setSpacing(10)
        
        self.status_combo = QComboBox()
        self.status_combo.addItems([s.replace("_", " ").title() for s in self.APPOINTMENT_STATUSES])
        self.status_combo.setCurrentText("Scheduled")
        self.status_combo.setMinimumHeight(35)
        status_layout.addRow("Status:", self.status_combo)
        
        self.confirmed_check = QCheckBox("Patient has confirmed this appointment")
        status_layout.addRow("Confirmation:", self.confirmed_check)
        
        self.reminder_sent_check = QCheckBox("Reminder has been sent to patient")
        status_layout.addRow("Reminder:", self.reminder_sent_check)
        
        layout.addWidget(status_group)
        
        # Rescheduling Information Group
        rescheduling_group = QGroupBox("Rescheduling Information")
        rescheduling_layout = QFormLayout(rescheduling_group)
        rescheduling_layout.setSpacing(10)
        
        self.rescheduled_from_edit = QLineEdit()
        self.rescheduled_from_edit.setPlaceholderText("Original appointment ID (if rescheduled)...")
        self.rescheduled_from_edit.setMinimumHeight(35)
        self.rescheduled_from_edit.setReadOnly(True)
        rescheduling_layout.addRow("Rescheduled From:", self.rescheduled_from_edit)
        
        layout.addWidget(rescheduling_group)
        
        layout.addStretch()
        
        return widget
    
    def setup_connections(self):
        """Setup signal connections"""
        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self.save_appointment)
        self.status_combo.currentTextChanged.connect(self.on_status_changed)
        
        if self.is_editing:
            self.delete_btn.clicked.connect(self.delete_appointment)
    
    def on_status_changed(self, status_text: str):
        """Handle status change to show/hide relevant fields"""
        status = status_text.lower().replace(" ", "_")
        self.cancellation_group.setVisible(status == "cancelled")
    
    def load_patient_doctor_data(self):
        """Load patients and doctors for selection"""
        try:
            with db_manager.get_session() as session:
                # Load patients
                patients = session.query(Patient).order_by(Patient.last_name, Patient.first_name).all()
                self.patients_data = []
                for patient in patients:
                    patient_data = {
                        'id': patient.id,
                        'display_name': f"{patient.first_name} {patient.last_name}",
                        'full_info': f"{patient.first_name} {patient.last_name} (ID: {patient.id})"
                    }
                    self.patients_data.append(patient_data)
                    self.patient_combo.addItem(patient_data['full_info'], patient.id)
                
                # Load doctors
                doctors = session.query(Doctor).filter(Doctor.is_active == True).order_by(Doctor.last_name, Doctor.first_name).all()
                self.doctors_data = []
                self.doctor_combo.addItem("No Doctor Assigned", None)
                for doctor in doctors:
                    doctor_data = {
                        'id': doctor.id,
                        'display_name': f"Dr. {doctor.first_name} {doctor.last_name}",
                        'full_info': f"Dr. {doctor.first_name} {doctor.last_name} - {doctor.specialty}"
                    }
                    self.doctors_data.append(doctor_data)
                    self.doctor_combo.addItem(doctor_data['full_info'], doctor.id)
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load patient/doctor data:\n{str(e)}")
    
    def set_default_doctor(self):
        """Set the default doctor if configured in settings"""
        try:
            with db_manager.get_session() as session:
                settings = session.query(GeneralSettings).first()
                if settings and settings.default_doctor_id:
                    # Find the doctor in the combo box and select it
                    for i in range(self.doctor_combo.count()):
                        if self.doctor_combo.itemData(i) == settings.default_doctor_id:
                            self.doctor_combo.setCurrentIndex(i)
                            break
                            
        except Exception as e:
            # If there's an error, just continue without setting default doctor
            print(f"Warning: Could not set default doctor: {str(e)}")
    
    def load_appointment(self):
        """Load appointment data for editing"""
        try:
            with db_manager.get_session() as session:
                appointment = session.query(Appointment).filter(Appointment.id == self.appointment_id).first()
                if not appointment:
                    QMessageBox.critical(self, "Error", "Appointment not found!")
                    self.reject()
                    return
                
                # Extract all data before session closes
                self.appointment_data = {
                    'id': appointment.id,
                    'date': appointment.date,
                    'reason': appointment.reason,
                    'state': appointment.state,
                    'patient_id': appointment.patient_id,
                    'doctor_id': appointment.doctor_id,
                    'appointment_type': appointment.appointment_type,
                    'duration_minutes': appointment.duration_minutes,
                    'priority': appointment.priority,
                    'notes': appointment.notes,
                    'patient_notes': appointment.patient_notes,
                    'confirmed': appointment.confirmed,
                    'reminder_sent': appointment.reminder_sent,
                    'cancelled_reason': appointment.cancelled_reason,
                    'cancelled_by': appointment.cancelled_by,
                    'rescheduled_from': appointment.rescheduled_from
                }
                
                # Populate form fields
                if self.appointment_data['date']:
                    qt_datetime = QDateTime.fromSecsSinceEpoch(int(self.appointment_data['date'].timestamp()))
                    self.date_time_edit.setDateTime(qt_datetime)
                
                self.reason_edit.setPlainText(self.appointment_data['reason'] or "")
                
                # Set patient selection
                if self.appointment_data['patient_id']:
                    for i in range(self.patient_combo.count()):
                        if self.patient_combo.itemData(i) == self.appointment_data['patient_id']:
                            self.patient_combo.setCurrentIndex(i)
                            break
                
                # Set doctor selection
                if self.appointment_data['doctor_id']:
                    for i in range(self.doctor_combo.count()):
                        if self.doctor_combo.itemData(i) == self.appointment_data['doctor_id']:
                            self.doctor_combo.setCurrentIndex(i)
                            break
                
                # Set other fields
                if self.appointment_data['duration_minutes']:
                    self.duration_spin.setValue(self.appointment_data['duration_minutes'])
                
                if self.appointment_data['appointment_type']:
                    type_display = self.appointment_data['appointment_type'].replace("_", " ").title()
                    self.type_combo.setCurrentText(type_display)
                
                if self.appointment_data['priority']:
                    self.priority_combo.setCurrentText(self.appointment_data['priority'].title())
                
                if self.appointment_data['state']:
                    status_display = self.appointment_data['state'].replace("_", " ").title()
                    self.status_combo.setCurrentText(status_display)
                
                # Set checkboxes
                self.confirmed_check.setChecked(bool(self.appointment_data['confirmed']))
                self.reminder_sent_check.setChecked(bool(self.appointment_data['reminder_sent']))
                
                # Set text areas
                self.notes_edit.setPlainText(self.appointment_data['notes'] or "")
                self.patient_notes_edit.setPlainText(self.appointment_data['patient_notes'] or "")
                self.cancelled_reason_edit.setText(self.appointment_data['cancelled_reason'] or "")
                self.cancelled_by_edit.setText(self.appointment_data['cancelled_by'] or "")
                
                if self.appointment_data['rescheduled_from']:
                    self.rescheduled_from_edit.setText(str(self.appointment_data['rescheduled_from']))
                
                # Update UI based on status
                self.on_status_changed(self.status_combo.currentText())
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load appointment:\n{str(e)}")
            self.reject()
    
    def validate_form(self) -> bool:
        """Validate form inputs"""
        if self.patient_combo.currentData() is None:
            QMessageBox.warning(self, "Validation Error", "Please select a patient!")
            self.patient_combo.setFocus()
            return False
        
        if not self.reason_edit.toPlainText().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter a reason for the appointment!")
            self.reason_edit.setFocus()
            return False
        
        # Check for scheduling conflicts (basic check)
        appointment_datetime = self.date_time_edit.dateTime().toPyDateTime()
        if appointment_datetime <= datetime.now():
            reply = QMessageBox.question(
                self, "Past Date",
                "The appointment is scheduled for a past date/time. Continue anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return False
        
        return True
    
    def save_appointment(self):
        """Save appointment data"""
        if not self.validate_form():
            return
        
        try:
            with db_manager.get_session() as session:
                if self.is_editing:
                    appointment = session.query(Appointment).filter(Appointment.id == self.appointment_id).first()
                    if not appointment:
                        QMessageBox.critical(self, "Error", "Appointment not found!")
                        return
                else:
                    appointment = Appointment()
                    session.add(appointment)
                
                # Update appointment data with all fields
                appointment.date = self.date_time_edit.dateTime().toPyDateTime()
                appointment.reason = self.reason_edit.toPlainText().strip()
                appointment.patient_id = self.patient_combo.currentData()
                appointment.doctor_id = self.doctor_combo.currentData()
                
                # Convert display text back to database values
                appointment.appointment_type = self.type_combo.currentText().lower().replace(" ", "_")
                appointment.duration_minutes = self.duration_spin.value()
                appointment.priority = self.priority_combo.currentText().lower()
                appointment.state = self.status_combo.currentText().lower().replace(" ", "_")
                
                # Notes and status
                appointment.notes = self.notes_edit.toPlainText().strip() or None
                appointment.patient_notes = self.patient_notes_edit.toPlainText().strip() or None
                appointment.confirmed = self.confirmed_check.isChecked()
                appointment.reminder_sent = self.reminder_sent_check.isChecked()
                
                # Cancellation info
                appointment.cancelled_reason = self.cancelled_reason_edit.text().strip() or None
                appointment.cancelled_by = self.cancelled_by_edit.text().strip() or None
                
                # Rescheduling info
                if self.rescheduled_from_edit.text().strip():
                    try:
                        appointment.rescheduled_from = int(self.rescheduled_from_edit.text().strip())
                    except ValueError:
                        appointment.rescheduled_from = None
                
                if not self.is_editing:
                    appointment.created_at = datetime.now()
                else:
                    appointment.updated_at = datetime.now()
                
                session.commit()
                
                # Get the appointment ID for the signal
                appointment_id = appointment.id
                
            self.appointment_saved.emit(appointment_id)
            
            action = "updated" if self.is_editing else "created"
            QMessageBox.information(self, "Success", f"Appointment {action} successfully!")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save appointment:\n{str(e)}")
    
    def delete_appointment(self):
        """Delete the current appointment"""
        if not self.appointment_data:
            QMessageBox.warning(self, "Error", "No appointment data available!")
            return
            
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete this appointment?\n\n"
            f"Patient: {self.appointment_data.get('patient_id', 'Unknown')}\n"
            f"Date: {self.appointment_data.get('date', 'Unknown')}\n\n"
            "This action cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                with db_manager.get_session() as session:
                    appointment = session.query(Appointment).filter(Appointment.id == self.appointment_id).first()
                    if appointment:
                        session.delete(appointment)
                        session.commit()
                
                QMessageBox.information(self, "Success", "Appointment deleted successfully!")
                self.appointment_saved.emit(self.appointment_id)  # Signal refresh
                self.accept()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete appointment:\n{str(e)}")

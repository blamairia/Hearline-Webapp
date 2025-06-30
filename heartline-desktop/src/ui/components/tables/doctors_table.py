"""
Doctors Table Widget for Heartline Desktop Application

This widget displays all doctors in a table format with search and filtering capabilities.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QHeaderView, QLineEdit, QLabel, QMessageBox,
    QComboBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import List, Optional, Dict

from src.models.complete_models import Doctor
from src.core.database import db_manager
from src.ui.styles import AppColors, AppStyles
from src.ui.doctor_management.dialogs.doctor_dialog import DoctorDialog

class DoctorsTableWidget(QWidget):
    """Widget for displaying and managing doctors table"""
    
    # Signals
    doctor_selected = pyqtSignal(int)  # Emitted when doctor is selected
    doctor_edit_requested = pyqtSignal(int)  # Emitted when edit is requested
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.doctors: List[Dict] = []  # Changed from List[Doctor] to List[Dict]
        self.setup_ui()
        self.setup_connections()
        self.load_doctors()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Apply comprehensive styling to the whole widget
        self.setStyleSheet(AppStyles.APP_STYLE)
        
        # Title
        title_label = QLabel("👨‍⚕️ Doctors Management")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {AppColors.PRIMARY}; margin: 10px;")
        layout.addWidget(title_label)
        
        # Search and filter section
        filter_frame = QFrame()
        filter_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        filter_layout = QHBoxLayout(filter_frame)
        
        # Search box
        filter_layout.addWidget(QLabel("🔍 Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, specialty, email, or phone...")
        filter_layout.addWidget(self.search_input)
        
        # Specialty filter
        filter_layout.addWidget(QLabel("Specialty:"))
        self.specialty_filter = QComboBox()
        self.specialty_filter.addItem("All Specialties")
        filter_layout.addWidget(self.specialty_filter)
        
        # Status filter
        filter_layout.addWidget(QLabel("Status:"))
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Active", "Inactive"])
        filter_layout.addWidget(self.status_filter)
        
        # Refresh button
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.load_doctors)
        filter_layout.addWidget(self.refresh_btn)
        
        # Add button
        self.add_btn = QPushButton("➕ Add Doctor")
        self.add_btn.clicked.connect(self.add_doctor)
        filter_layout.addWidget(self.add_btn)
        
        # Edit button
        self.edit_btn = QPushButton("✏️ Edit Doctor")
        self.edit_btn.clicked.connect(self.edit_selected_doctor)
        self.edit_btn.setEnabled(False)  # Disabled until selection
        filter_layout.addWidget(self.edit_btn)
        
        layout.addWidget(filter_frame)
        
        # Table
        self.table = QTableWidget()
        self.setup_table()
        layout.addWidget(self.table)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #666; margin: 5px;")
        layout.addWidget(self.status_label)
    
    def setup_table(self):
        """Setup the table widget"""
        headers = [
            "ID", "First Name", "Last Name", "Specialty", "Phone", 
            "Email", "License", "Experience", "Education", "Certifications",
            "Fee", "Office", "Address", "Emergency Contact", "Status", "Updated", "Created"
        ]
        
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # First Name
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Last Name
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)          # Specialty
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Phone
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)          # Email
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # License
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)  # Experience
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.Stretch)          # Education
        header.setSectionResizeMode(9, QHeaderView.ResizeMode.Stretch)          # Certifications
        header.setSectionResizeMode(10, QHeaderView.ResizeMode.ResizeToContents) # Fee
        header.setSectionResizeMode(11, QHeaderView.ResizeMode.ResizeToContents) # Office
        header.setSectionResizeMode(12, QHeaderView.ResizeMode.Stretch)         # Address
        header.setSectionResizeMode(13, QHeaderView.ResizeMode.ResizeToContents) # Emergency Contact
        header.setSectionResizeMode(14, QHeaderView.ResizeMode.ResizeToContents) # Status
        header.setSectionResizeMode(15, QHeaderView.ResizeMode.ResizeToContents) # Updated
        header.setSectionResizeMode(16, QHeaderView.ResizeMode.ResizeToContents) # Created
        
        # Set row selection behavior
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        
        # Apply table styling
        self.table.setStyleSheet(AppStyles.get_table_style())
        
        # Make table headers bold
        header = self.table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.search_input.textChanged.connect(self.filter_table)
        self.specialty_filter.currentTextChanged.connect(self.filter_table)
        self.status_filter.currentTextChanged.connect(self.filter_table)
        self.table.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
    
    def load_doctors(self):
        """Load doctors from database"""
        try:
            self.status_label.setText("Loading doctors...")
            
            # Get database session
            with db_manager.get_session() as session:
                # Query doctors using SQLAlchemy
                doctors_query = session.query(Doctor).order_by(Doctor.last_name, Doctor.first_name).all()
                
                # Extract data from SQLAlchemy objects before session closes
                self.doctors = []
                specialties = set()
                
                for doctor in doctors_query:
                    doctor_data = {
                        'id': doctor.id,
                        'first_name': doctor.first_name,
                        'last_name': doctor.last_name,
                        'specialty': doctor.specialty,
                        'phone': doctor.phone,
                        'email': doctor.email,
                        'license_number': doctor.license_number,
                        'years_of_experience': doctor.years_of_experience,
                        'education': doctor.education,
                        'certifications': doctor.certifications,
                        'consultation_fee': doctor.consultation_fee,
                        'office_number': doctor.office_number,
                        'address': doctor.address,
                        'emergency_contact': doctor.emergency_contact,
                        'bio': doctor.bio,
                        'schedule_notes': doctor.schedule_notes,
                        'is_active': doctor.is_active,
                        'created_at': doctor.created_at,
                        'updated_at': doctor.updated_at
                    }
                    self.doctors.append(doctor_data)
                    if doctor.specialty:
                        specialties.add(doctor.specialty)
            
            # Update specialty filter
            self.update_specialty_filter(specialties)
            
            self.populate_table()
            self.status_label.setText(f"✅ Loaded {len(self.doctors)} doctors")
            
        except Exception as e:
            self.status_label.setText(f"❌ Error loading doctors: {str(e)}")
            QMessageBox.critical(self, "Database Error", f"Failed to load doctors:\n{str(e)}")
    
    def update_specialty_filter(self, specialties):
        """Update the specialty filter with available specialties"""
        current_specialty = self.specialty_filter.currentText()
        self.specialty_filter.clear()
        self.specialty_filter.addItem("All Specialties")
        
        for specialty in sorted(specialties):
            self.specialty_filter.addItem(specialty)
        
        # Restore previous selection if it still exists
        index = self.specialty_filter.findText(current_specialty)
        if index >= 0:
            self.specialty_filter.setCurrentIndex(index)
    
    def populate_table(self):
        """Populate table with doctor data"""
        self.table.setRowCount(len(self.doctors))
        
        for row, doctor in enumerate(self.doctors):
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(doctor['id'])))
            
            # First Name
            self.table.setItem(row, 1, QTableWidgetItem(doctor['first_name'] or ""))
            
            # Last Name
            self.table.setItem(row, 2, QTableWidgetItem(doctor['last_name'] or ""))
            
            # Specialty
            self.table.setItem(row, 3, QTableWidgetItem(doctor['specialty'] or ""))
            
            # Phone
            self.table.setItem(row, 4, QTableWidgetItem(doctor['phone'] or ""))
            
            # Email
            self.table.setItem(row, 5, QTableWidgetItem(doctor['email'] or ""))
            
            # License Number
            self.table.setItem(row, 6, QTableWidgetItem(doctor['license_number'] or ""))
            
            # Years of Experience
            experience = f"{doctor['years_of_experience']} years" if doctor['years_of_experience'] else ""
            self.table.setItem(row, 7, QTableWidgetItem(experience))
            
            # Education (truncated for display)
            education = doctor['education'] or ""
            if len(education) > 50:
                education = education[:50] + "..."
            self.table.setItem(row, 8, QTableWidgetItem(education))
            
            # Certifications (truncated for display)
            certifications = doctor['certifications'] or ""
            if len(certifications) > 50:
                certifications = certifications[:50] + "..."
            self.table.setItem(row, 9, QTableWidgetItem(certifications))
            
            # Consultation Fee
            fee = f"${doctor['consultation_fee']:.2f}" if doctor['consultation_fee'] else ""
            self.table.setItem(row, 10, QTableWidgetItem(fee))
            
            # Office Number
            self.table.setItem(row, 11, QTableWidgetItem(doctor['office_number'] or ""))
            
            # Address (truncated for display)
            address = doctor['address'] or ""
            if len(address) > 30:
                address = address[:30] + "..."
            self.table.setItem(row, 12, QTableWidgetItem(address))
            
            # Emergency Contact
            emergency_contact = doctor['emergency_contact'] or ""
            if len(emergency_contact) > 25:
                emergency_contact = emergency_contact[:25] + "..."
            self.table.setItem(row, 13, QTableWidgetItem(emergency_contact))
            
            # Status
            status_text = "Active" if doctor['is_active'] else "Inactive" if doctor['is_active'] is False else ""
            item = QTableWidgetItem(status_text)
            if doctor['is_active']:
                item.setBackground(Qt.GlobalColor.green)
            elif doctor['is_active'] is False:
                item.setBackground(Qt.GlobalColor.lightGray)
            self.table.setItem(row, 14, item)
            
            # Updated At
            updated_str = doctor['updated_at'].strftime("%Y-%m-%d") if doctor['updated_at'] else ""
            self.table.setItem(row, 15, QTableWidgetItem(updated_str))
            
            # Created At
            created_str = doctor['created_at'].strftime("%Y-%m-%d") if doctor['created_at'] else ""
            self.table.setItem(row, 16, QTableWidgetItem(created_str))
    
    def filter_table(self):
        """Filter table based on search input and filters"""
        search_text = self.search_input.text().lower()
        specialty_filter = self.specialty_filter.currentText()
        status_filter = self.status_filter.currentText()
        
        for row in range(self.table.rowCount()):
            should_show = True
            
            # Apply search filter
            if search_text:
                text_match = False
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item and search_text in item.text().lower():
                        text_match = True
                        break
                if not text_match:
                    should_show = False
            
            # Apply specialty filter
            if should_show and specialty_filter != "All Specialties":
                specialty_item = self.table.item(row, 3)  # Specialty column
                if not specialty_item or specialty_item.text() != specialty_filter:
                    should_show = False
            
            # Apply status filter
            if should_show and status_filter != "All":
                status_item = self.table.item(row, 14)  # Status column (index 14)
                if status_item:
                    if status_filter == "Active" and status_item.text() != "Active":
                        should_show = False
                    elif status_filter == "Inactive" and status_item.text() != "Inactive":
                        should_show = False
            
            self.table.setRowHidden(row, not should_show)
    
    def on_item_double_clicked(self, item):
        """Handle item double click - edit doctor"""
        row = item.row()
        doctor_id = int(self.table.item(row, 0).text())
        self.edit_doctor(doctor_id)
    
    def on_selection_changed(self):
        """Handle selection change"""
        current_row = self.table.currentRow()
        has_selection = current_row >= 0
        
        # Enable/disable edit button based on selection
        self.edit_btn.setEnabled(has_selection)
        
        if has_selection:
            doctor_id = int(self.table.item(current_row, 0).text())
            self.doctor_selected.emit(doctor_id)
    
    def edit_doctor(self, doctor_id: Optional[int] = None):
        """Edit selected doctor"""
        if doctor_id is None:
            doctor_id = self.get_selected_doctor_id()
        
        if doctor_id is None:
            QMessageBox.warning(self, "No Selection", "Please select a doctor to edit.")
            return
            
        dialog = DoctorDialog(doctor_id=doctor_id, parent=self)
        dialog.doctor_saved.connect(self.load_doctors)  # Refresh table when doctor is saved
        dialog.exec()

    def add_doctor(self):
        """Add new doctor"""
        dialog = DoctorDialog(parent=self)
        dialog.doctor_saved.connect(self.load_doctors)  # Refresh table when doctor is saved
        dialog.exec()
    
    def edit_selected_doctor(self):
        """Edit the currently selected doctor"""
        doctor_id = self.get_selected_doctor_id()
        if doctor_id:
            self.edit_doctor(doctor_id)
    
    def get_selected_doctor_id(self) -> Optional[int]:
        """Get the ID of currently selected doctor"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            return int(self.table.item(current_row, 0).text())
        return None
    
    def refresh_data(self):
        """Refresh the doctor data"""
        self.load_doctors()

class DoctorManagementWidget(QWidget):
    """Main widget for doctor management with table and controls"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI for doctor management"""
        layout = QVBoxLayout(self)
        
        # Add the doctors table
        self.doctors_table = DoctorsTableWidget()
        layout.addWidget(self.doctors_table)

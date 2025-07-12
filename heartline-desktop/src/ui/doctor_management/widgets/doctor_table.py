"""
Simple Doctor Table Widget

Basic table view for doctors without complex filtering or bulk actions.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QHeaderView, QLineEdit, QLabel, QMessageBox,
    QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import List, Dict

from src.models.complete_models import Doctor
from src.core.database import db_manager
from src.ui.styles import AppColors, AppStyles


class DoctorTableWidget(QWidget):
    """Simple widget for displaying and managing doctors table"""
    
    # Signals
    doctor_selected = pyqtSignal(int)  # Emitted when doctor is selected
    doctor_edit_requested = pyqtSignal(int)  # Emitted when edit is requested
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.doctors: List[Dict] = []
        self.setup_ui()
        self.setup_connections()
        self.load_doctors()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Apply comprehensive styling to match patient management
        self.setStyleSheet(AppStyles.APP_STYLE)
        
        # Title
        title_label = QLabel("👨‍⚕️ Doctors Management")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {AppColors.PRIMARY}; margin: 10px;")
        layout.addWidget(title_label)
        
        # Simple search and action section
        action_frame = QFrame()
        action_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        action_layout = QHBoxLayout(action_frame)
        
        # Search box
        action_layout.addWidget(QLabel("🔍 Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, specialty, or phone...")
        action_layout.addWidget(self.search_input)
        
        action_layout.addStretch()
        
        # Action buttons
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.add_btn = QPushButton("➕ Add Doctor")
        self.edit_btn = QPushButton("✏️ Edit Doctor")
        self.edit_btn.setEnabled(False)
        
        action_layout.addWidget(self.refresh_btn)
        action_layout.addWidget(self.add_btn)
        action_layout.addWidget(self.edit_btn)
        
        layout.addWidget(action_frame)
        
        # Table
        self.table = QTableWidget()
        self.setup_table()
        layout.addWidget(self.table)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #666; margin: 5px;")
        layout.addWidget(self.status_label)
    
    def setup_table(self):
        """Setup the table widget with exact same styling as patient table"""
        headers = [
            "ID", "First Name", "Last Name", "Specialty", "Phone", 
            "Email", "License", "Experience", "Fee", "Status", "Created"
        ]
        
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        # Table properties - match patient table exactly
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        
        # Set column widths
        column_widths = [60, 120, 120, 140, 120, 180, 120, 100, 80, 80, 120]
        for i, width in enumerate(column_widths):
            self.table.setColumnWidth(i, width)
        
        # Make table headers bold and apply same styling as patient table
        header = self.table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        
        # Apply exact same table styling as patient management
        self.table.setStyleSheet(AppStyles.get_table_style())
    
    def setup_connections(self):
        """Setup signal connections"""
        self.search_input.textChanged.connect(self.filter_doctors)
        self.refresh_btn.clicked.connect(self.load_doctors)
        self.add_btn.clicked.connect(self.add_doctor)
        self.edit_btn.clicked.connect(self.edit_selected_doctor)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        self.table.itemDoubleClicked.connect(self.on_double_click)
    
    def load_doctors(self):
        """Load all doctors from database"""
        try:
            self.status_label.setText("Loading doctors...")
            
            with db_manager.get_session() as session:
                doctors = session.query(Doctor).order_by(Doctor.last_name, Doctor.first_name).all()
                
                # Extract data before session closes
                self.doctors = []
                for doctor in doctors:
                    doctor_data = {
                        'id': doctor.id,
                        'first_name': doctor.first_name,
                        'last_name': doctor.last_name,
                        'specialty': doctor.specialty,
                        'phone': doctor.phone,
                        'email': doctor.email,
                        'license_number': doctor.license_number,
                        'years_experience': doctor.years_experience,
                        'consultation_fee': doctor.consultation_fee,
                        'status': doctor.status,
                        'created_at': doctor.created_at
                    }
                    self.doctors.append(doctor_data)
                
                self.populate_table(self.doctors)
                
            self.status_label.setText(f"Loaded {len(self.doctors)} doctors")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load doctors:\n{str(e)}")
            self.status_label.setText("Error loading doctors")
    
    def populate_table(self, doctors: List[Dict]):
        """Populate table with doctor data"""
        self.table.setRowCount(len(doctors))
        
        for row, doctor in enumerate(doctors):
            # ID
            item = QTableWidgetItem(str(doctor['id']))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, item)
            
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
            
            # License
            self.table.setItem(row, 6, QTableWidgetItem(doctor['license_number'] or ""))
            
            # Experience
            exp_text = f"{doctor['years_experience']} years" if doctor['years_experience'] else ""
            self.table.setItem(row, 7, QTableWidgetItem(exp_text))
            
            # Fee
            fee_text = f"${doctor['consultation_fee']:.0f}" if doctor['consultation_fee'] else ""
            self.table.setItem(row, 8, QTableWidgetItem(fee_text))
            
            # Status
            status_item = QTableWidgetItem(doctor['status'] or "Unknown")
            status_color = AppColors.get_status_color(doctor['status'] or "unknown")
            status_item.setForeground(AppColors.get_qcolor(status_color))
            self.table.setItem(row, 9, status_item)
            
            # Created
            created_text = doctor['created_at'].strftime("%Y-%m-%d") if doctor['created_at'] else ""
            self.table.setItem(row, 10, QTableWidgetItem(created_text))
    
    def filter_doctors(self):
        """Filter doctors based on search text"""
        search_text = self.search_input.text().lower()
        
        if not search_text:
            self.populate_table(self.doctors)
            return
        
        filtered_doctors = []
        for doctor in self.doctors:
            # Search in name, specialty, and phone
            search_fields = [
                doctor['first_name'] or "",
                doctor['last_name'] or "",
                doctor['specialty'] or "",
                doctor['phone'] or ""
            ]
            
            if any(search_text in field.lower() for field in search_fields):
                filtered_doctors.append(doctor)
        
        self.populate_table(filtered_doctors)
        self.status_label.setText(f"Showing {len(filtered_doctors)} of {len(self.doctors)} doctors")
    
    def on_selection_changed(self):
        """Handle table selection change"""
        selected_items = self.table.selectedItems()
        self.edit_btn.setEnabled(len(selected_items) > 0)
        
        if selected_items:
            row = selected_items[0].row()
            doctor_id = int(self.table.item(row, 0).text())
            self.doctor_selected.emit(doctor_id)
    
    def on_double_click(self, item):
        """Handle double click on table item"""
        row = item.row()
        doctor_id = int(self.table.item(row, 0).text())
        self.doctor_edit_requested.emit(doctor_id)
    
    def add_doctor(self):
        """Add new doctor"""
        from ..dialogs import DoctorDialog
        
        dialog = DoctorDialog(parent=self)
        dialog.doctor_saved.connect(self.load_doctors)
        dialog.exec()
    
    def edit_selected_doctor(self):
        """Edit selected doctor"""
        selected_items = self.table.selectedItems()
        if not selected_items:
            return
        
        row = selected_items[0].row()
        doctor_id = int(self.table.item(row, 0).text())
        
        from ..dialogs import DoctorDialog
        
        dialog = DoctorDialog(doctor_id=doctor_id, parent=self)
        dialog.doctor_saved.connect(self.load_doctors)
        dialog.exec()
    
    def get_selected_doctor_id(self) -> int:
        """Get the ID of the currently selected doctor"""
        selected_items = self.table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            return int(self.table.item(row, 0).text())
        return None
    
    def refresh(self):
        """Refresh the table data"""
        self.load_doctors()

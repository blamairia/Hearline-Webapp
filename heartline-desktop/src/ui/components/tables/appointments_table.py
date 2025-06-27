"""
Appointments Table Widget for Heartline Desktop Application

This widget displays all appointments in a table format with search and filtering capabilities.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QHeaderView, QLineEdit, QLabel, QMessageBox,
    QComboBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import List, Optional

from src.models.complete_models import Appointment
from src.core.database import db_manager

class AppointmentsTableWidget(QWidget):
    """Widget for displaying and managing appointments table"""
    
    # Signals
    appointment_selected = pyqtSignal(int)  # Emitted when appointment is selected
    appointment_edit_requested = pyqtSignal(int)  # Emitted when edit is requested
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.appointments: List[Appointment] = []
        self.setup_ui()
        self.setup_connections()
        self.load_appointments()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("📅 Appointments Management")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2196F3; margin: 10px;")
        layout.addWidget(title_label)
        
        # Search and filter section
        filter_frame = QFrame()
        filter_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        filter_layout = QHBoxLayout(filter_frame)
        
        # Search box
        filter_layout.addWidget(QLabel("🔍 Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by reason, patient, or doctor...")
        filter_layout.addWidget(self.search_input)
        
        # State filter
        filter_layout.addWidget(QLabel("State:"))
        self.state_filter = QComboBox()
        self.state_filter.addItems(["All", "Scheduled", "Completed", "Cancelled", "No-show"])
        filter_layout.addWidget(self.state_filter)
        
        # Refresh button
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.load_appointments)
        filter_layout.addWidget(self.refresh_btn)
        
        # Add button
        self.add_btn = QPushButton("➕ Add Appointment")
        self.add_btn.clicked.connect(self.add_appointment)
        filter_layout.addWidget(self.add_btn)
        
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
            "ID", "Date", "Reason", "State", "Patient ID", "Doctor ID", "Created", "Updated"
        ]
        
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Date
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)          # Reason
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # State
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Patient ID
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Doctor ID
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Created
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)  # Updated
        
        # Set row selection behavior
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        
        # Make table headers bold
        header = self.table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.search_input.textChanged.connect(self.filter_table)
        self.state_filter.currentTextChanged.connect(self.filter_table)
        self.table.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
    
    def load_appointments(self):
        """Load appointments from database"""
        try:
            self.status_label.setText("Loading appointments...")
            
            # Get database session
            with db_manager.get_session() as session:
                # Query appointments using SQLAlchemy
                appointments_query = session.query(Appointment).order_by(Appointment.date.desc()).all()
                
                # Extract data from SQLAlchemy objects before session closes
                self.appointments = []
                for appointment in appointments_query:
                    appointment_data = {
                        'id': appointment.id,
                        'patient_id': appointment.patient_id,
                        'doctor_id': appointment.doctor_id,
                        'date': appointment.date,
                        'reason': appointment.reason,
                        'state': appointment.state,
                        'created_at': appointment.created_at,
                        'updated_at': appointment.updated_at
                    }
                    self.appointments.append(appointment_data)
            
            self.populate_table()
            self.status_label.setText(f"✅ Loaded {len(self.appointments)} appointments")
            
        except Exception as e:
            self.status_label.setText(f"❌ Error loading appointments: {str(e)}")
            QMessageBox.critical(self, "Database Error", f"Failed to load appointments:\n{str(e)}")
    
    def populate_table(self):
        """Populate table with appointment data"""
        self.table.setRowCount(len(self.appointments))
        
        for row, appointment in enumerate(self.appointments):
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(appointment['id'])))
            
            # Date
            date_str = appointment['date'].strftime("%Y-%m-%d %H:%M") if appointment['date'] else ""
            self.table.setItem(row, 1, QTableWidgetItem(date_str))
            
            # Reason
            self.table.setItem(row, 2, QTableWidgetItem(appointment['reason'] or ""))
            
            # State
            state_item = QTableWidgetItem(appointment['state'] or "")
            # Color code states
            if appointment['state'] == "Completed":
                state_item.setBackground(Qt.GlobalColor.green)
            elif appointment['state'] == "Cancelled":
                state_item.setBackground(Qt.GlobalColor.red)
            elif appointment['state'] == "Scheduled":
                state_item.setBackground(Qt.GlobalColor.blue)
            self.table.setItem(row, 3, state_item)
            
            # Patient ID
            self.table.setItem(row, 4, QTableWidgetItem(str(appointment['patient_id'])))
            
            # Doctor ID
            doctor_id = str(appointment['doctor_id']) if appointment['doctor_id'] else ""
            self.table.setItem(row, 5, QTableWidgetItem(doctor_id))
            
            # Created At
            created_str = appointment['created_at'].strftime("%Y-%m-%d %H:%M") if appointment['created_at'] else ""
            self.table.setItem(row, 6, QTableWidgetItem(created_str))
            
            # Updated At
            updated_str = appointment['updated_at'].strftime("%Y-%m-%d %H:%M") if appointment['updated_at'] else ""
            self.table.setItem(row, 7, QTableWidgetItem(updated_str))
    
    def filter_table(self):
        """Filter table based on search input and filters"""
        search_text = self.search_input.text().lower()
        state_filter = self.state_filter.currentText()
        
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
            
            # Apply state filter
            if should_show and state_filter != "All":
                state_item = self.table.item(row, 3)  # State column
                if not state_item or state_item.text() != state_filter:
                    should_show = False
            
            self.table.setRowHidden(row, not should_show)
    
    def on_item_double_clicked(self, item):
        """Handle item double click"""
        row = item.row()
        appointment_id = int(self.table.item(row, 0).text())
        self.appointment_edit_requested.emit(appointment_id)
    
    def on_selection_changed(self):
        """Handle selection change"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            appointment_id = int(self.table.item(current_row, 0).text())
            self.appointment_selected.emit(appointment_id)
    
    def add_appointment(self):
        """Add new appointment"""
        # This will be implemented when we add CRUD functionality
        QMessageBox.information(self, "Add Appointment", "Add appointment functionality will be implemented in the next phase.")
    
    def get_selected_appointment_id(self) -> Optional[int]:
        """Get the ID of currently selected appointment"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            return int(self.table.item(current_row, 0).text())
        return None
    
    def refresh_data(self):
        """Refresh the appointment data"""
        self.load_appointments()

class AppointmentManagementWidget(QWidget):
    """Main widget for appointment management with table and controls"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI for appointment management"""
        layout = QVBoxLayout(self)
        
        # Add the appointments table
        self.appointments_table = AppointmentsTableWidget()
        layout.addWidget(self.appointments_table)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        
        # Configure headers
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)
        
        # Set font
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)
        
        # Connect signals
        self.itemSelectionChanged.connect(self.on_selection_changed)
    
    def load_data(self):
        """Load appointments data from database"""
        try:
            appointments = self.repository.get_all()
            self.populate_table(appointments)
        except Exception as e:
            print(f"Error loading appointments: {e}")
            self.setRowCount(0)
    
    def populate_table(self, appointments: List[Appointment]):
        """Populate table with appointments data"""
        self.setRowCount(len(appointments))
        
        for row, appointment in enumerate(appointments):
            for col, (header, attr) in enumerate(self.columns):
                value = getattr(appointment, attr, "")
                
                # Format values
                if attr in ["date", "created_at"] and value:
                    value = value.strftime("%Y-%m-%d %H:%M")
                elif value is None:
                    value = ""
                
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Read-only
                
                # Store appointment object in the first column
                if col == 0:
                    item.setData(Qt.ItemDataRole.UserRole, appointment)
                
                self.setItem(row, col, item)
    
    def on_selection_changed(self):
        """Handle selection change"""
        current_row = self.currentRow()
        if current_row >= 0:
            item = self.item(current_row, 0)  # Get first column item
            if item:
                appointment = item.data(Qt.ItemDataRole.UserRole)
                if appointment:
                    self.appointment_selected.emit(appointment)
    
    def refresh(self):
        """Refresh the table data"""
        self.load_data()
    
    def get_selected_appointment(self) -> Optional[Appointment]:
        """Get the currently selected appointment"""
        current_row = self.currentRow()
        if current_row >= 0:
            item = self.item(current_row, 0)
            if item:
                return item.data(Qt.ItemDataRole.UserRole)
        return None


class AppointmentManagementWidget(QWidget):
    """Widget for managing appointments with table view"""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the widget UI"""
        layout = QVBoxLayout()
        
        # Create table
        self.appointments_table = AppointmentsTableWidget()
        layout.addWidget(self.appointments_table)
        
        self.setLayout(layout)
    
    def refresh(self):
        """Refresh the appointments data"""
        self.appointments_table.refresh()

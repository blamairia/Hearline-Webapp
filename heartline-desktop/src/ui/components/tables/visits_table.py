"""
Visits Table Widget for Heartline Desktop Application

This widget displays all visits in a table format with search and filtering capabilities.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QHeaderView, QLineEdit, QLabel, QMessageBox,
    QComboBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import List, Optional

from src.models.complete_models import Visit
from src.core.database import db_manager

class VisitsTableWidget(QWidget):
    """Widget for displaying and managing visits table"""
    
    # Signals
    visit_selected = pyqtSignal(int)  # Emitted when visit is selected
    visit_edit_requested = pyqtSignal(int)  # Emitted when edit is requested
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.visits: List[Visit] = []
        self.setup_ui()
        self.setup_connections()
        self.load_visits()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("🏥 Visits Management")
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
        self.search_input.setPlaceholderText("Search by diagnosis, patient, or doctor...")
        filter_layout.addWidget(self.search_input)
        
        # Status filter
        filter_layout.addWidget(QLabel("Status:"))
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Completed", "In Progress", "Cancelled"])
        filter_layout.addWidget(self.status_filter)
        
        # Refresh button
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.load_visits)
        filter_layout.addWidget(self.refresh_btn)
        
        # Add button
        self.add_btn = QPushButton("➕ Add Visit")
        self.add_btn.clicked.connect(self.add_visit)
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
            "ID", "Patient ID", "Doctor ID", "Visit Date", "Diagnosis", 
            "Follow-up", "Payment", "Status", "Created"
        ]
        
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Patient ID
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Doctor ID
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Visit Date
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)          # Diagnosis
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Follow-up
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Payment
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)  # Status
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents)  # Created
        
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
        self.status_filter.currentTextChanged.connect(self.filter_table)
        self.table.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
    
    def load_visits(self):
        """Load visits from database"""
        try:
            self.status_label.setText("Loading visits...")
            
            # Get database session
            with db_manager.get_session() as session:
                # Query visits using SQLAlchemy
                visits_query = session.query(Visit).order_by(Visit.visit_date.desc()).all()
                
                # Extract data from SQLAlchemy objects before session closes
                self.visits = []
                for visit in visits_query:
                    visit_data = {
                        'id': visit.id,
                        'patient_id': visit.patient_id,
                        'doctor_id': visit.doctor_id,
                        'visit_date': visit.visit_date,
                        'diagnosis': visit.diagnosis,
                        'follow_up_date': visit.follow_up_date,
                        'payment_total': visit.payment_total,
                        'payment_status': visit.payment_status,
                        'visit_status': visit.visit_status,
                        'created_at': visit.created_at
                    }
                    self.visits.append(visit_data)
            
            self.populate_table()
            self.status_label.setText(f"✅ Loaded {len(self.visits)} visits")
            
        except Exception as e:
            self.status_label.setText(f"❌ Error loading visits: {str(e)}")
            QMessageBox.critical(self, "Database Error", f"Failed to load visits:\n{str(e)}")
    
    def populate_table(self):
        """Populate table with visit data"""
        self.table.setRowCount(len(self.visits))
        
        for row, visit in enumerate(self.visits):
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(visit['id'])))
            
            # Patient ID
            self.table.setItem(row, 1, QTableWidgetItem(str(visit['patient_id'])))
            
            # Doctor ID
            doctor_id = str(visit['doctor_id']) if visit['doctor_id'] else ""
            self.table.setItem(row, 2, QTableWidgetItem(doctor_id))
            
            # Visit Date
            visit_date_str = visit['visit_date'].strftime("%Y-%m-%d %H:%M") if visit['visit_date'] else ""
            self.table.setItem(row, 3, QTableWidgetItem(visit_date_str))
            
            # Diagnosis
            self.table.setItem(row, 4, QTableWidgetItem(visit['diagnosis'] or ""))
            
            # Follow-up Date
            followup_str = visit['follow_up_date'].strftime("%Y-%m-%d") if visit['follow_up_date'] else ""
            self.table.setItem(row, 5, QTableWidgetItem(followup_str))
            
            # Payment
            payment = f"${visit['payment_total']:.2f}" if visit['payment_total'] else ""
            self.table.setItem(row, 6, QTableWidgetItem(payment))
            
            # Status
            status_item = QTableWidgetItem(visit['visit_status'] or "")
            if visit['visit_status'] == "Completed":
                status_item.setBackground(Qt.GlobalColor.green)
            elif visit['visit_status'] == "In Progress":
                status_item.setBackground(Qt.GlobalColor.blue)
            elif visit['visit_status'] == "Cancelled":
                status_item.setBackground(Qt.GlobalColor.red)
            self.table.setItem(row, 7, status_item)
            
            # Created At
            created_str = visit['created_at'].strftime("%Y-%m-%d") if visit['created_at'] else ""
            self.table.setItem(row, 8, QTableWidgetItem(created_str))
    
    def filter_table(self):
        """Filter table based on search input and filters"""
        search_text = self.search_input.text().lower()
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
            
            # Apply status filter
            if should_show and status_filter != "All":
                status_item = self.table.item(row, 7)  # Status column
                if not status_item or status_item.text() != status_filter:
                    should_show = False
            
            self.table.setRowHidden(row, not should_show)
    
    def on_item_double_clicked(self, item):
        """Handle item double click"""
        row = item.row()
        visit_id = int(self.table.item(row, 0).text())
        self.visit_edit_requested.emit(visit_id)
    
    def on_selection_changed(self):
        """Handle selection change"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            visit_id = int(self.table.item(current_row, 0).text())
            self.visit_selected.emit(visit_id)
    
    def add_visit(self):
        """Add new visit"""
        # This will be implemented when we add CRUD functionality
        QMessageBox.information(self, "Add Visit", "Add visit functionality will be implemented in the next phase.")
    
    def get_selected_visit_id(self) -> Optional[int]:
        """Get the ID of currently selected visit"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            return int(self.table.item(current_row, 0).text())
        return None
    
    def refresh_data(self):
        """Refresh the visit data"""
        self.load_visits()

class VisitManagementWidget(QWidget):
    """Main widget for visit management with table and controls"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI for visit management"""
        layout = QVBoxLayout(self)
        
        # Add the visits table
        self.visits_table = VisitsTableWidget()
        layout.addWidget(self.visits_table)
    
    def setup_ui(self):
        """Set up the table UI with enhanced fields"""
        # Define columns including enhanced fields
        self.columns = [
            ("ID", "id"),
            ("Visit Date", "visit_date"),
            ("Patient ID", "patient_id"),
            ("Doctor ID", "doctor_id"),
            ("Type", "visit_type"),
            ("Duration", "visit_duration"),
            ("Chief Complaint", "chief_complaint"),
            ("Blood Pressure", "blood_pressure"),
            ("Heart Rate", "heart_rate"),
            ("Diagnosis", "diagnosis"),
            ("Status", "visit_status"),
            ("Payment", "payment_status"),
            ("Total", "payment_total"),
            ("Created At", "created_at")
        ]
        
        # Set up table
        self.setColumnCount(len(self.columns))
        self.setHorizontalHeaderLabels([col[0] for col in self.columns])
        
        # Configure table behavior
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
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
        """Load visits data from database"""
        try:
            visits = self.repository.get_all()
            self.populate_table(visits)
        except Exception as e:
            print(f"Error loading visits: {e}")
            self.setRowCount(0)
    
    def populate_table(self, visits: List[Visit]):
        """Populate table with visits data including enhanced fields"""
        self.setRowCount(len(visits))
        
        for row, visit in enumerate(visits):
            for col, (header, attr) in enumerate(self.columns):
                value = getattr(visit, attr, "")
                
                # Format values
                if attr in ["visit_date", "created_at"] and value:
                    value = value.strftime("%Y-%m-%d %H:%M")
                elif attr == "visit_duration" and value:
                    value = f"{value} min"
                elif attr == "heart_rate" and value:
                    value = f"{value} bpm"
                elif attr == "payment_total" and value:
                    value = f"${value:.2f}"
                elif attr in ["diagnosis", "chief_complaint"] and value:
                    # Truncate long text
                    value = value[:30] + "..." if len(str(value)) > 30 else value
                elif value is None:
                    value = "N/A"
                else:
                    value = str(value)
                
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Read-only
                
                # Store visit object in the first column
                if col == 0:
                    item.setData(Qt.ItemDataRole.UserRole, visit)
                
                self.setItem(row, col, item)
    
    def on_selection_changed(self):
        """Handle selection change"""
        current_row = self.currentRow()
        if current_row >= 0:
            item = self.item(current_row, 0)  # Get first column item
            if item:
                visit = item.data(Qt.ItemDataRole.UserRole)
                if visit:
                    self.visit_selected.emit(visit)
    
    def refresh(self):
        """Refresh the table data"""
        self.load_data()
    
    def get_selected_visit(self) -> Optional[Visit]:
        """Get the currently selected visit"""
        current_row = self.currentRow()
        if current_row >= 0:
            item = self.item(current_row, 0)
            if item:
                return item.data(Qt.ItemDataRole.UserRole)
        return None


class VisitManagementWidget(QWidget):
    """Widget for managing visits with table view"""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the widget UI"""
        layout = QVBoxLayout()
        
        # Create table
        self.visits_table = VisitsTableWidget()
        layout.addWidget(self.visits_table)
        
        self.setLayout(layout)
    
    def refresh(self):
        """Refresh the visits data"""
        self.visits_table.refresh()

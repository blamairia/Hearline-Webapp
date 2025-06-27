"""
Waiting list table widget for displaying all waiting list entries
"""

from typing import List, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QHeaderView, QLineEdit, QLabel, QMessageBox,
    QComboBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from src.models.complete_models import WaitingListEntry
from src.core.database import db_manager
from src.ui.styles import AppColors, AppStyles


class WaitingListTableWidget(QWidget):
    """Widget for displaying and managing waiting list table"""
    
    # Signals
    waiting_list_entry_selected = pyqtSignal(int)  # Emitted when an entry is selected
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.waiting_list_entries: List[dict] = []
        self.setup_ui()
        self.setup_connections()
        self.load_waiting_list()
    
    def setup_ui(self):
        """Set up the table UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("⏳ Waiting List Management")
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
        self.search_input.setPlaceholderText("Search by patient ID or status...")
        filter_layout.addWidget(self.search_input)
        
        # Status filter
        filter_layout.addWidget(QLabel("Status:"))
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Waiting", "Called", "In Progress", "Completed"])
        filter_layout.addWidget(self.status_filter)
        
        # Refresh button
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.load_waiting_list)
        filter_layout.addWidget(self.refresh_btn)
        
        layout.addWidget(filter_frame)
        
        # Table
        self.table = QTableWidget()
        self.setup_table()
        layout.addWidget(self.table)
        
        # Status label
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
    
    def setup_table(self):
        """Setup the table widget"""
        headers = [
            "ID", "Patient ID", "Arrival Time", "Status", "Priority", 
            "Assigned Doctor", "Created At"
        ]
        
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Patient ID
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)          # Arrival Time
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Status
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Priority
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)          # Assigned Doctor
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Created At
        
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
    
    def load_waiting_list(self):
        """Load waiting list entries from database"""
        try:
            self.status_label.setText("Loading waiting list...")
            
            # Get database session
            with db_manager.get_session() as session:
                # Query waiting list entries using SQLAlchemy
                entries_query = session.query(WaitingListEntry).order_by(WaitingListEntry.arrival_time.desc()).all()
                
                # Extract data from SQLAlchemy objects before session closes
                self.waiting_list_entries = []
                for entry in entries_query:
                    entry_data = {
                        'id': entry.id,
                        'patient_id': entry.patient_id,
                        'arrival_time': entry.arrival_time,
                        'status': entry.status,
                        'priority': entry.priority,
                        'assigned_doctor': entry.assigned_doctor,
                        'created_at': entry.created_at
                    }
                    self.waiting_list_entries.append(entry_data)
            
            self.populate_table()
            self.status_label.setText(f"✅ Loaded {len(self.waiting_list_entries)} waiting list entries")
            
        except Exception as e:
            self.status_label.setText(f"❌ Error loading waiting list: {str(e)}")
            QMessageBox.critical(self, "Database Error", f"Failed to load waiting list:\n{str(e)}")
    
    def populate_table(self):
        """Populate table with waiting list data"""
        self.table.setRowCount(len(self.waiting_list_entries))
        
        for row, entry in enumerate(self.waiting_list_entries):
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(entry['id'])))
            
            # Patient ID
            self.table.setItem(row, 1, QTableWidgetItem(str(entry['patient_id'])))
            
            # Arrival Time
            arrival_str = entry['arrival_time'].strftime("%Y-%m-%d %H:%M") if entry['arrival_time'] else ""
            self.table.setItem(row, 2, QTableWidgetItem(arrival_str))
            
            # Status
            status_item = QTableWidgetItem(entry['status'] or "")
            # Color code status
            if entry['status'] == "Waiting":
                status_item.setBackground(Qt.GlobalColor.yellow)
            elif entry['status'] == "Called":
                status_item.setBackground(Qt.GlobalColor.cyan)
            elif entry['status'] == "In Progress":
                status_item.setBackground(Qt.GlobalColor.blue)
            elif entry['status'] == "Completed":
                status_item.setBackground(Qt.GlobalColor.green)
            self.table.setItem(row, 3, status_item)
            
            # Priority
            self.table.setItem(row, 4, QTableWidgetItem(str(entry['priority']) if entry['priority'] else ""))
            
            # Assigned Doctor
            self.table.setItem(row, 5, QTableWidgetItem(str(entry['assigned_doctor']) if entry['assigned_doctor'] else ""))
            
            # Created At
            created_str = entry['created_at'].strftime("%Y-%m-%d %H:%M") if entry['created_at'] else ""
            self.table.setItem(row, 6, QTableWidgetItem(created_str))
    
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
                status_item = self.table.item(row, 3)  # Status column
                if not status_item or status_item.text() != status_filter:
                    should_show = False
            
            self.table.setRowHidden(row, not should_show)
    
    def on_item_double_clicked(self, item):
        """Handle item double click"""
        row = item.row()
        entry_id = int(self.table.item(row, 0).text())
        # Could emit a signal for editing
        
    def on_selection_changed(self):
        """Handle selection change"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            entry_id = int(self.table.item(current_row, 0).text())
            self.waiting_list_entry_selected.emit(entry_id)
    
    def refresh_data(self):
        """Refresh the waiting list data"""
        self.load_waiting_list()


class WaitingListManagementWidget(QWidget):
    """Main widget for waiting list management with table and controls"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI for waiting list management"""
        layout = QVBoxLayout(self)
        
        # Add the waiting list table
        self.waiting_list_table = WaitingListTableWidget()
        layout.addWidget(self.waiting_list_table)

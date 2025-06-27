"""
Dashboard Widget for Heartline Desktop Application

This module provides the main dashboard with statistics, recent activities,
and quick access to common functions.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPalette

class StatCard(QFrame):
    """A statistics card widget"""
    
    def __init__(self, title, value, icon="", color="#2196F3"):
        super().__init__()
        self.setup_ui(title, value, icon, color)
    
    def setup_ui(self, title, value, icon, color):
        """Setup the stat card UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Value
        value_label = QLabel(str(value))
        value_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {color};")
        layout.addWidget(value_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12))
        title_label.setStyleSheet("color: #666;")
        layout.addWidget(title_label)
        
        # Styling
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)
        self.setFixedHeight(100)

class DashboardWidget(QWidget):
    """Main dashboard widget"""
    
    # Signals
    action_requested = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_timer()
    
    def setup_ui(self):
        """Setup the dashboard UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Dashboard")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_data)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Statistics cards
        stats_layout = QGridLayout()
        
        # Create stat cards (placeholder data)
        self.total_patients_card = StatCard("Total Patients", "150", "👥", "#4CAF50")
        self.appointments_today_card = StatCard("Appointments Today", "12", "📅", "#FF9800")
        self.ecg_tests_card = StatCard("ECG Tests This Week", "45", "🔬", "#9C27B0")
        self.revenue_card = StatCard("Monthly Revenue", "125,000 DZD", "💰", "#2196F3")
        
        stats_layout.addWidget(self.total_patients_card, 0, 0)
        stats_layout.addWidget(self.appointments_today_card, 0, 1)
        stats_layout.addWidget(self.ecg_tests_card, 0, 2)
        stats_layout.addWidget(self.revenue_card, 0, 3)
        
        layout.addLayout(stats_layout)
        
        # Content area
        content_layout = QHBoxLayout()
        
        # Recent activities
        recent_frame = self.create_recent_activities()
        content_layout.addWidget(recent_frame, 2)
        
        # Quick actions
        actions_frame = self.create_quick_actions()
        content_layout.addWidget(actions_frame, 1)
        
        layout.addLayout(content_layout)
        
        # Add stretch to push everything to top
        layout.addStretch()
    
    def create_recent_activities(self):
        """Create recent activities widget"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Header
        header_label = QLabel("Recent Activities")
        header_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(header_label)
        
        # Activities table
        self.activities_table = QTableWidget()
        self.activities_table.setColumnCount(3)
        self.activities_table.setHorizontalHeaderLabels(["Time", "Activity", "Patient"])
        self.activities_table.horizontalHeader().setStretchLastSection(True)
        self.activities_table.setAlternatingRowColors(True)
        self.activities_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # Sample data
        activities = [
            ("10:30 AM", "ECG Analysis Completed", "John Doe"),
            ("10:15 AM", "Appointment Scheduled", "Mary Smith"),
            ("09:45 AM", "Visit Documented", "Ahmed Ali"),
            ("09:30 AM", "Prescription Created", "Sarah Johnson"),
            ("09:15 AM", "Patient Registered", "Omar Hassan"),
        ]
        
        self.activities_table.setRowCount(len(activities))
        for row, (time, activity, patient) in enumerate(activities):
            self.activities_table.setItem(row, 0, QTableWidgetItem(time))
            self.activities_table.setItem(row, 1, QTableWidgetItem(activity))
            self.activities_table.setItem(row, 2, QTableWidgetItem(patient))
        
        layout.addWidget(self.activities_table)
        
        return frame
    
    def create_quick_actions(self):
        """Create quick actions widget"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Header
        header_label = QLabel("Quick Actions")
        header_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(header_label)
        
        # Action buttons
        actions = [
            ("👥 New Patient", "new_patient", "#4CAF50"),
            ("📅 Schedule Appointment", "new_appointment", "#2196F3"),
            ("📋 Create Visit", "new_visit", "#FF9800"),
            ("🔬 ECG Analysis", "ecg_analysis", "#9C27B0"),
            ("💊 Create Prescription", "new_prescription", "#795548"),
            ("📊 View Reports", "reports", "#607D8B"),
        ]
        
        for text, action, color in actions:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, a=action: self.action_requested.emit(a))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 12px 16px;
                    font-weight: bold;
                    text-align: left;
                    margin-bottom: 4px;
                }}
                QPushButton:hover {{
                    opacity: 0.8;
                }}
            """)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        return frame
    
    def setup_timer(self):
        """Setup timer for periodic updates"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.refresh_data)
        self.update_timer.start(60000)  # Update every minute
    
    def refresh_data(self):
        """Refresh dashboard data"""
        # TODO: Implement actual data fetching from database
        # For now, this is a placeholder
        
        # Update statistics (placeholder)
        # self.total_patients_card.update_value("152")
        # self.appointments_today_card.update_value("14")
        
        # Update activities table
        # self.load_recent_activities()
        
        pass
    
    def load_recent_activities(self):
        """Load recent activities from database"""
        # TODO: Implement database query for recent activities
        pass

"""
Navigation Panel for Heartline Desktop Application

This module provides the main navigation panel with menu items and quick actions.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QFrame, QScrollArea, QButtonGroup
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

from src.ui.styles import AppColors, AppStyles

class NavigationPanel(QWidget):
    """Left navigation panel with menu items"""
    
    # Signals
    page_requested = pyqtSignal(str)  # Emitted when a page is requested
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_connections()
    
    def setup_ui(self):
        """Setup the navigation panel UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Apply comprehensive styling
        self.setStyleSheet(AppStyles.APP_STYLE)
        
        # Header section
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {AppColors.PRIMARY_DARK};
                color: {AppColors.TEXT_ON_PRIMARY};
                padding: 16px;
            }}
        """)
        header_layout = QVBoxLayout(header_frame)
        
        # Logo/Title
        title_label = QLabel("Heartline")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {AppColors.TEXT_ON_PRIMARY}; margin-bottom: 4px;")
        header_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Desktop")
        subtitle_label.setFont(QFont("Arial", 12))
        subtitle_label.setStyleSheet(f"color: {AppColors.PRIMARY_LIGHT};")
        header_layout.addWidget(subtitle_label)
        
        layout.addWidget(header_frame)
        
        # Navigation buttons
        nav_frame = QFrame()
        nav_frame.setObjectName("navigation")
        nav_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-right: 1px solid #ddd;
            }
        """)
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(8, 8, 8, 8)
        nav_layout.setSpacing(4)
        
        # Create button group for exclusive selection
        self.button_group = QButtonGroup()
        
        # Navigation items
        nav_items = [
            ("dashboard", "📊 Dashboard", True),
            ("patients", "👥 Patients", False),
            ("doctors", "👨‍⚕️ Doctors", False),
            ("appointments", "📅 Appointments", False),
            ("visits", "📋 Visits", False),
            ("waiting_list", "⏳ Waiting List", False),
            ("prescriptions", "💊 Prescriptions", False),
            ("medicaments", "� Medicaments", False),
            ("visit_documents", "� Visit Documents", False),
            ("ecg", "🔬 ECG Analysis", False),
            ("users", "� Users", False),
            ("clinic_info", "🏥 Clinic Info", False),
            ("general_settings", "⚙️ General Settings", False),
            ("reports", "📈 Reports", False),
        ]
        
        for page_id, text, is_default in nav_items:
            btn = self.create_nav_button(page_id, text)
            if is_default:
                btn.setChecked(True)
            self.button_group.addButton(btn)
            nav_layout.addWidget(btn)
        
        nav_layout.addStretch()
        
        # Quick actions section
        quick_actions_label = QLabel("Quick Actions")
        quick_actions_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        quick_actions_label.setStyleSheet("color: #666; margin-top: 16px; margin-bottom: 8px;")
        nav_layout.addWidget(quick_actions_label)
        
        # Quick action buttons
        new_patient_btn = QPushButton("+ New Patient")
        new_patient_btn.clicked.connect(lambda: self.page_requested.emit('new_patient'))
        new_patient_btn.setStyleSheet(self.get_quick_action_style())
        nav_layout.addWidget(new_patient_btn)
        
        new_appointment_btn = QPushButton("+ New Appointment")
        new_appointment_btn.clicked.connect(lambda: self.page_requested.emit('new_appointment'))
        new_appointment_btn.setStyleSheet(self.get_quick_action_style())
        nav_layout.addWidget(new_appointment_btn)
        
        layout.addWidget(nav_frame)
        
        # Apply overall styling
        self.setStyleSheet("""
            NavigationPanel {
                background-color: white;
                border-right: 1px solid #e0e0e0;
            }
        """)
    
    def create_nav_button(self, page_id, text):
        """Create a navigation button"""
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setProperty("page_id", page_id)
        btn.setObjectName("nav_button")
        btn.clicked.connect(lambda: self.page_requested.emit(page_id))
        
        # Set minimum height and styling for better visibility
        btn.setMinimumHeight(40)
        btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 8px 12px;
                border: none;
                background-color: transparent;
                color: #333;
                font-size: 14px;
                border-radius: 4px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QPushButton:checked {
                background-color: #2196f3;
                color: white;
                font-weight: bold;
            }
        """)
        
        return btn
    
    def get_quick_action_style(self):
        """Get styling for quick action buttons"""
        return """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 12px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """
    
    def setup_connections(self):
        """Setup signal connections"""
        pass  # Connections are set up in button creation
    
    def set_active_page(self, page_id):
        """Set the active page in navigation"""
        for button in self.button_group.buttons():
            if button.property("page_id") == page_id:
                button.setChecked(True)
                break

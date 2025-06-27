"""
Main Window for Heartline Desktop Application

This module contains the main application window with navigation,
toolbar, status bar, and content areas.
"""

import sys
import logging
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QStackedWidget, QStatusBar, QMenuBar, QToolBar, QLabel,
    QMessageBox, QSplitter, QFrame, QGridLayout, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QIcon, QPixmap, QFont

from ..core.database import db_manager
from .styles import AppColors, AppStyles
from .components.navigation import NavigationPanel
from .components.dashboard import DashboardWidget
from .patient_management import PatientManagementWidget
from .components.appointments import AppointmentWidget
from .components.visits import VisitManagementWidget
from .components.ecg_analysis import ECGAnalysisWidget
from .components.database_tables import DatabaseTablesWidget
from .components.tables import (
    DoctorsTableWidget, WaitingListTableWidget, PrescriptionsTableWidget,
    MedicamentsTableWidget, VisitDocumentsTableWidget, UsersTableWidget,
    ClinicInfoTableWidget, GeneralSettingsTableWidget
)
from .dialogs.login_dialog import LoginDialog

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """Main application window"""
    
    # Signals
    user_logged_in = pyqtSignal(object)  # Emitted when user logs in
    user_logged_out = pyqtSignal()       # Emitted when user logs out
    
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.setup_ui()
        self.setup_connections()
        self.show_login()
    
    def setup_ui(self):
        """Setup the main window UI"""
        self.setWindowTitle("Heartline Desktop - Doctor Cabinet Management")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Create navigation panel
        self.navigation_panel = NavigationPanel()
        self.navigation_panel.setMaximumWidth(250)
        self.navigation_panel.setMinimumWidth(200)
        splitter.addWidget(self.navigation_panel)
        
        # Create content area
        self.content_widget = QStackedWidget()
        splitter.addWidget(self.content_widget)
        
        # Set splitter proportions
        splitter.setSizes([250, 1150])
        
        # Create content widgets
        self.create_content_widgets()
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create status bar
        self.create_status_bar()
        
        # Apply custom styling
        self.apply_styling()
    
    def create_content_widgets(self):
        """Create all content widgets for the stacked widget"""
        
        # Dashboard
        self.dashboard_widget = DashboardWidget()
        self.content_widget.addWidget(self.dashboard_widget)
        
        # Patient Management
        self.patient_widget = PatientManagementWidget()
        self.content_widget.addWidget(self.patient_widget)
        
        # Doctors Management
        self.doctors_widget = DoctorsTableWidget()
        self.content_widget.addWidget(self.doctors_widget)
        
        # Appointments
        self.appointment_widget = AppointmentWidget()
        self.content_widget.addWidget(self.appointment_widget)
        
        # Visits
        self.visit_widget = VisitManagementWidget()
        self.content_widget.addWidget(self.visit_widget)
        
        # Waiting List
        self.waiting_list_widget = WaitingListTableWidget()
        self.content_widget.addWidget(self.waiting_list_widget)
        
        # Prescriptions
        self.prescriptions_widget = PrescriptionsTableWidget()
        self.content_widget.addWidget(self.prescriptions_widget)
        
        # Medicaments
        self.medicaments_widget = MedicamentsTableWidget()
        self.content_widget.addWidget(self.medicaments_widget)
        
        # Visit Documents
        self.visit_documents_widget = VisitDocumentsTableWidget()
        self.content_widget.addWidget(self.visit_documents_widget)
        
        # ECG Analysis
        self.ecg_widget = ECGAnalysisWidget()
        self.content_widget.addWidget(self.ecg_widget)
        
        # Users Management
        self.users_widget = UsersTableWidget()
        self.content_widget.addWidget(self.users_widget)
        
        # Clinic Information
        self.clinic_info_widget = ClinicInfoTableWidget()
        self.content_widget.addWidget(self.clinic_info_widget)
        
        # General Settings
        self.general_settings_widget = GeneralSettingsTableWidget()
        self.content_widget.addWidget(self.general_settings_widget)
        
        # Database Tables Management (keep as overview/fallback)
        self.database_tables_widget = DatabaseTablesWidget()
        self.content_widget.addWidget(self.database_tables_widget)
        
        # Set default widget
        self.content_widget.setCurrentWidget(self.dashboard_widget)
    
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('&File')
        
        # New actions
        new_patient_action = QAction('&New Patient', self)
        new_patient_action.setShortcut('Ctrl+N')
        new_patient_action.triggered.connect(self.new_patient)
        file_menu.addAction(new_patient_action)
        
        new_appointment_action = QAction('New &Appointment', self)
        new_appointment_action.setShortcut('Ctrl+A')
        new_appointment_action.triggered.connect(self.new_appointment)
        file_menu.addAction(new_appointment_action)
        
        file_menu.addSeparator()
        
        # Settings
        settings_action = QAction('&Settings', self)
        settings_action.triggered.connect(self.show_settings)
        file_menu.addAction(settings_action)
        
        file_menu.addSeparator()
        
        # Exit
        exit_action = QAction('E&xit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu('&View')
        
        dashboard_action = QAction('&Dashboard', self)
        dashboard_action.triggered.connect(lambda: self.show_page('dashboard'))
        view_menu.addAction(dashboard_action)
        
        patients_action = QAction('&Patients', self)
        patients_action.triggered.connect(lambda: self.show_page('patients'))
        view_menu.addAction(patients_action)
        
        appointments_action = QAction('&Appointments', self)
        appointments_action.triggered.connect(lambda: self.show_page('appointments'))
        view_menu.addAction(appointments_action)
        
        database_action = QAction('&Database Tables', self)
        database_action.triggered.connect(lambda: self.show_page('database_tables'))
        view_menu.addAction(database_action)
        
        # Tools menu
        tools_menu = menubar.addMenu('&Tools')
        
        ecg_action = QAction('&ECG Analysis', self)
        ecg_action.triggered.connect(lambda: self.show_page('ecg'))
        tools_menu.addAction(ecg_action)
        
        # Help menu
        help_menu = menubar.addMenu('&Help')
        
        about_action = QAction('&About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Create application toolbar"""
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        
        # Quick action buttons
        new_patient_btn = QPushButton("New Patient")
        new_patient_btn.clicked.connect(self.new_patient)
        toolbar.addWidget(new_patient_btn)
        
        new_appointment_btn = QPushButton("New Appointment")
        new_appointment_btn.clicked.connect(self.new_appointment)
        toolbar.addWidget(new_appointment_btn)
        
        toolbar.addSeparator()
        
        ecg_analysis_btn = QPushButton("ECG Analysis")
        ecg_analysis_btn.clicked.connect(lambda: self.show_page('ecg'))
        toolbar.addWidget(ecg_analysis_btn)
    
    def create_status_bar(self):
        """Create application status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Database status
        self.db_status_label = QLabel("Database: Connected")
        self.status_bar.addPermanentWidget(self.db_status_label)
        
        # User info
        self.user_label = QLabel("Not logged in")
        self.status_bar.addPermanentWidget(self.user_label)
        
        # Start status update timer
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(5000)  # Update every 5 seconds
    
    def setup_connections(self):
        """Setup signal connections"""
        # Navigation panel connections
        self.navigation_panel.page_requested.connect(self.show_page)
        
        # User authentication
        self.user_logged_in.connect(self.on_user_logged_in)
        self.user_logged_out.connect(self.on_user_logged_out)
    
    def apply_styling(self):
        """Apply custom styling to the main window"""
        # Apply the comprehensive app style
        self.setStyleSheet(AppStyles.APP_STYLE + f"""
            QToolBar {{
                background-color: {AppColors.SURFACE};
                border-bottom: 1px solid {AppColors.BORDER};
                padding: 4px;
            }}
            QToolBar QPushButton {{
                background-color: {AppColors.PRIMARY};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                margin: 2px;
                font-weight: bold;
            }}
            QToolBar QPushButton:hover {{
                background-color: {AppColors.PRIMARY_DARK};
            }}
            QStatusBar {{
                background-color: {AppColors.SURFACE};
                border-top: 1px solid {AppColors.BORDER};
                color: {AppColors.TEXT};
            }}
        """)
    
    def show_login(self):
        """Show login dialog"""
        login_dialog = LoginDialog(self)
        if login_dialog.exec() == QMessageBox.DialogCode.Accepted:
            self.current_user = login_dialog.get_user()
            self.user_logged_in.emit(self.current_user)
        else:
            sys.exit()
    
    def show_page(self, page_name):
        """Show the requested page"""
        widgets = {
            'dashboard': self.dashboard_widget,
            'patients': self.patient_widget,
            'doctors': self.doctors_widget,
            'appointments': self.appointment_widget,
            'visits': self.visit_widget,
            'waiting_list': self.waiting_list_widget,
            'prescriptions': self.prescriptions_widget,
            'medicaments': self.medicaments_widget,
            'visit_documents': self.visit_documents_widget,
            'ecg': self.ecg_widget,
            'users': self.users_widget,
            'clinic_info': self.clinic_info_widget,
            'general_settings': self.general_settings_widget,
            'database_tables': self.database_tables_widget,
            'tables': self.database_tables_widget,  # Alternative name
        }
        
        widget = widgets.get(page_name)
        if widget:
            self.content_widget.setCurrentWidget(widget)
            self.status_bar.showMessage(f"Showing {page_name.replace('_', ' ').title()}", 2000)
        else:
            self.status_bar.showMessage(f"Page '{page_name}' not found", 2000)
    
    def new_patient(self):
        """Create new patient"""
        self.show_page('patients')
        self.patient_widget.new_patient()
    
    def new_appointment(self):
        """Create new appointment"""
        self.show_page('appointments')
        self.appointment_widget.new_appointment()
    
    def show_settings(self):
        """Show application settings"""
        QMessageBox.information(self, "Settings", "Settings dialog will be implemented")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Heartline Desktop",
            "Heartline Desktop v1.0.0\n\n"
            "A comprehensive doctor cabinet management system\n"
            "with AI-powered ECG analysis.\n\n"
            "© 2024 Heartline Medical"
        )
    
    def on_user_logged_in(self, user):
        """Handle user login"""
        self.user_label.setText(f"User: {user.full_name} ({user.role})")
        logger.info(f"User logged in: {user.username}")
    
    def on_user_logged_out(self):
        """Handle user logout"""
        self.user_label.setText("Not logged in")
        self.current_user = None
        self.show_login()
    
    def update_status(self):
        """Update status bar information"""
        # Check database connection
        if db_manager.check_connection():
            self.db_status_label.setText("Database: Connected")
            self.db_status_label.setStyleSheet("color: green;")
        else:
            self.db_status_label.setText("Database: Disconnected")
            self.db_status_label.setStyleSheet("color: red;")
    
    def closeEvent(self, event):
        """Handle application close event"""
        reply = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to exit Heartline Desktop?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Cleanup
            db_manager.close()
            logger.info("Application closed")
            event.accept()
        else:
            event.ignore()

"""
Users Table Widget for Heartline Desktop Application

This widget displays all users in a table format with search and filtering capabilities.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QHeaderView, QLineEdit, QLabel, QMessageBox,
    QComboBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import List, Optional

from src.models.complete_models import User
from src.core.database import db_manager
from src.ui.styles import AppColors, AppStyles

class UsersTableWidget(QWidget):
    """Widget for displaying and managing users table"""
    
    # Signals
    user_selected = pyqtSignal(int)  # Emitted when user is selected
    user_edit_requested = pyqtSignal(int)  # Emitted when edit is requested
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.users: List[User] = []
        self.setup_ui()
        self.setup_connections()
        self.load_users()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Apply comprehensive styling to the whole widget
        self.setStyleSheet(AppStyles.APP_STYLE)
        
        # Title
        title_label = QLabel("👤 Users Management")
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
        self.search_input.setPlaceholderText("Search by username, email, or name...")
        filter_layout.addWidget(self.search_input)
        
        # Role filter
        filter_layout.addWidget(QLabel("Role:"))
        self.role_filter = QComboBox()
        self.role_filter.addItems(["All Roles", "doctor", "assistant"])
        filter_layout.addWidget(self.role_filter)
        
        # Status filter
        filter_layout.addWidget(QLabel("Status:"))
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All Status", "Active", "Inactive"])
        filter_layout.addWidget(self.status_filter)
        
        # Action buttons
        filter_layout.addStretch()
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.new_user_btn = QPushButton("➕ New User")
        self.edit_user_btn = QPushButton("✏️ Edit")
        self.deactivate_user_btn = QPushButton("🚫 Deactivate")
        
        self.refresh_btn.setObjectName("primary-button")
        self.new_user_btn.setObjectName("success-button")
        self.edit_user_btn.setObjectName("primary-button")
        self.deactivate_user_btn.setObjectName("danger-button")
        
        filter_layout.addWidget(self.refresh_btn)
        filter_layout.addWidget(self.new_user_btn)
        filter_layout.addWidget(self.edit_user_btn)
        filter_layout.addWidget(self.deactivate_user_btn)
        
        layout.addWidget(filter_frame)
        
        # Users table
        self.setup_table()
        layout.addWidget(self.users_table)
        
        # Status bar
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #666; padding: 5px;")
        layout.addWidget(self.status_label)
    
    def setup_table(self):
        """Setup the users table"""
        # Define columns
        self.columns = [
            ("ID", 60),
            ("Username", 120),
            ("Email", 180),
            ("Full Name", 150),
            ("Role", 100),
            ("Phone", 120),
            ("Status", 80),
            ("Last Login", 120),
            ("Created", 120)
        ]
        
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(len(self.columns))
        
        # Set headers and column widths
        headers = []
        for i, (header, width) in enumerate(self.columns):
            headers.append(header)
            self.users_table.setColumnWidth(i, width)
        
        self.users_table.setHorizontalHeaderLabels(headers)
        
        # Table properties
        self.users_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.users_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.users_table.setAlternatingRowColors(True)
        self.users_table.setSortingEnabled(True)
        
        # Apply table styling
        self.users_table.setStyleSheet(AppStyles.get_table_style())
        # Make table headers bold
        header = self.users_table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.search_input.textChanged.connect(self.filter_users)
        self.role_filter.currentTextChanged.connect(self.filter_users)
        self.status_filter.currentTextChanged.connect(self.filter_users)
        self.refresh_btn.clicked.connect(self.load_users)
        self.new_user_btn.clicked.connect(self.new_user)
        self.edit_user_btn.clicked.connect(self.edit_selected_user)
        self.deactivate_user_btn.clicked.connect(self.deactivate_selected_user)
        self.users_table.itemSelectionChanged.connect(self.on_selection_changed)
        self.users_table.itemDoubleClicked.connect(self.on_double_click)
    
    def load_users(self):
        """Load all users from database"""
        try:
            self.status_label.setText("Loading users...")
            
            with db_manager.get_session() as session:
                users = session.query(User).order_by(User.username).all()
                self.users = users
                self.populate_table(users)
                
            self.status_label.setText(f"Loaded {len(users)} users")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load users:\n{str(e)}")
            self.status_label.setText("Error loading users")
    
    def populate_table(self, users: List[User]):
        """Populate table with user data"""
        self.users_table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            # ID
            self.users_table.setItem(row, 0, QTableWidgetItem(str(user.id)))
            
            # Username
            self.users_table.setItem(row, 1, QTableWidgetItem(user.username))
            
            # Email
            self.users_table.setItem(row, 2, QTableWidgetItem(user.email))
            
            # Full Name
            full_name = user.full_name
            self.users_table.setItem(row, 3, QTableWidgetItem(full_name))
            
            # Role
            role = user.role.title() if user.role else "N/A"
            self.users_table.setItem(row, 4, QTableWidgetItem(role))
            
            # Phone
            phone = user.phone or "N/A"
            self.users_table.setItem(row, 5, QTableWidgetItem(phone))
            
            # Status
            status = "Active" if user.is_active else "Inactive"
            self.users_table.setItem(row, 6, QTableWidgetItem(status))
            
            # Last Login
            last_login = user.last_login.strftime("%Y-%m-%d %H:%M") if user.last_login else "Never"
            self.users_table.setItem(row, 7, QTableWidgetItem(last_login))
            
            # Created
            created = user.created_at.strftime("%Y-%m-%d") if user.created_at else "N/A"
            self.users_table.setItem(row, 8, QTableWidgetItem(created))
            
            # Store user ID in first column for reference
            self.users_table.item(row, 0).setData(Qt.ItemDataRole.UserRole, user.id)
    
    def filter_users(self):
        """Filter users based on search criteria"""
        search_text = self.search_input.text().lower()
        role_filter = self.role_filter.currentText()
        status_filter = self.status_filter.currentText()
        
        filtered_users = []
        
        for user in self.users:
            # Text search
            if search_text:
                searchable_text = f"{user.username} {user.email} {user.first_name} {user.last_name}".lower()
                if search_text not in searchable_text:
                    continue
            
            # Role filter
            if role_filter != "All Roles" and user.role != role_filter.lower():
                continue
            
            # Status filter
            if status_filter == "Active" and not user.is_active:
                continue
            elif status_filter == "Inactive" and user.is_active:
                continue
            
            filtered_users.append(user)
        
        self.populate_table(filtered_users)
        self.status_label.setText(f"Showing {len(filtered_users)} of {len(self.users)} users")
    
    def on_selection_changed(self):
        """Handle selection change"""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            item = self.users_table.item(current_row, 0)
            if item:
                user_id = item.data(Qt.ItemDataRole.UserRole)
                if user_id:
                    self.user_selected.emit(user_id)
        
        # Enable/disable action buttons
        has_selection = current_row >= 0
        self.edit_user_btn.setEnabled(has_selection)
        self.deactivate_user_btn.setEnabled(has_selection)
    
    def on_double_click(self, item):
        """Handle double click"""
        self.edit_selected_user()
    
    def new_user(self):
        """Create new user"""
        # TODO: Open user creation dialog
        QMessageBox.information(self, "New User", "User creation dialog will be implemented here.")
    
    def edit_selected_user(self):
        """Edit selected user"""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            item = self.users_table.item(current_row, 0)
            if item:
                user_id = item.data(Qt.ItemDataRole.UserRole)
                if user_id:
                    self.user_edit_requested.emit(user_id)
    
    def deactivate_selected_user(self):
        """Deactivate selected user"""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            reply = QMessageBox.question(
                self, "Confirm Deactivation", 
                "Are you sure you want to deactivate this user?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # TODO: Implement user deactivation
                QMessageBox.information(self, "Deactivate User", "User deactivation will be implemented here.")
                self.load_users()  # Refresh table
    
    def get_selected_user_id(self) -> Optional[int]:
        """Get the currently selected user ID"""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            item = self.users_table.item(current_row, 0)
            if item:
                return item.data(Qt.ItemDataRole.UserRole)
        return None

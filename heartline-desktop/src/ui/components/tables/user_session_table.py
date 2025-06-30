"""
User Session Table Widget for Heartline Desktop Application

This widget displays user sessions in a table format with search and filtering capabilities.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QHeaderView, QLineEdit, QLabel, QMessageBox,
    QComboBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import List, Optional

from src.models.complete_models import UserSession
from src.core.database import db_manager

class UserSessionTableWidget(QWidget):
    """Widget for displaying and managing user_session table"""
    
    # Signals
    session_selected = pyqtSignal(int)  # Emitted when session is selected
    session_edit_requested = pyqtSignal(int)  # Emitted when edit is requested
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sessions: List[UserSession] = []
        self.setup_ui()
        self.setup_connections()
        self.load_sessions()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("🔐 User Sessions")
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
        self.search_input.setPlaceholderText("Search by user ID, IP address, or token...")
        filter_layout.addWidget(self.search_input)
        
        # Status filter
        filter_layout.addWidget(QLabel("Status:"))
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Active", "Inactive"])
        filter_layout.addWidget(self.status_filter)
        
        # Refresh button
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.load_sessions)
        filter_layout.addWidget(self.refresh_btn)
        
        # Clean expired button
        self.clean_btn = QPushButton("🧹 Clean Expired")
        self.clean_btn.clicked.connect(self.clean_expired_sessions)
        filter_layout.addWidget(self.clean_btn)
        
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
            "ID", "User ID", "Session Token", "IP Address", 
            "User Agent", "Active", "Created", "Expires"
        ]
        
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # User ID
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)          # Session Token
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # IP Address
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)          # User Agent
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Active
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Created
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)  # Expires
        
        # Set row selection behavior
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        
        # Style the table
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: #f5f5f5;
                selection-background-color: #e3f2fd;
                gridline-color: #ddd;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QHeaderView::section {
                background-color: #2196F3;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.search_input.textChanged.connect(self.filter_table)
        self.status_filter.currentTextChanged.connect(self.filter_table)
        self.table.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
    
    def load_sessions(self):
        """Load sessions from database"""
        try:
            self.status_label.setText("Loading user sessions...")
            
            # Get database session
            with db_manager.get_session() as session:
                # Query sessions with user info using SQLAlchemy
                from src.models.complete_models import User
                sessions_query = session.query(UserSession, User.username).join(
                    User, UserSession.user_id == User.id, isouter=True
                ).order_by(UserSession.created_at.desc()).all()
                
                # Convert to list
                self.sessions = []
                for session_data, username in sessions_query:
                    # Add username for display
                    session_data.username = username
                    self.sessions.append(session_data)
            
            self.populate_table()
            self.status_label.setText(f"✅ Loaded {len(self.sessions)} session records")
            
        except Exception as e:
            self.status_label.setText(f"❌ Error loading sessions: {str(e)}")
            QMessageBox.critical(self, "Database Error", f"Failed to load user sessions:\n{str(e)}")
    
    def populate_table(self):
        """Populate table with session data"""
        self.table.setRowCount(len(self.sessions))
        
        for row, session in enumerate(self.sessions):
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(session.id)))
            
            # User ID (with username if available)
            user_display = f"{session.user_id}"
            if hasattr(session, 'username') and session.username:
                user_display += f" ({session.username})"
            self.table.setItem(row, 1, QTableWidgetItem(user_display))
            
            # Session Token (truncated for display)
            token_display = session.session_token[:32] + "..." if len(session.session_token) > 32 else session.session_token
            self.table.setItem(row, 2, QTableWidgetItem(token_display))
            
            # IP Address
            self.table.setItem(row, 3, QTableWidgetItem(session.ip_address or ""))
            
            # User Agent (truncated for display)
            user_agent = session.user_agent or ""
            if len(user_agent) > 50:
                user_agent = user_agent[:50] + "..."
            self.table.setItem(row, 4, QTableWidgetItem(user_agent))
            
            # Active
            active_text = "Yes" if session.is_active else "No" if session.is_active is False else ""
            item = QTableWidgetItem(active_text)
            if session.is_active:
                item.setBackground(Qt.GlobalColor.lightGreen)
            elif session.is_active is False:
                item.setBackground(Qt.GlobalColor.lightGray)
            self.table.setItem(row, 5, item)
            
            # Created At
            created_str = session.created_at.strftime("%Y-%m-%d %H:%M") if session.created_at else ""
            self.table.setItem(row, 6, QTableWidgetItem(created_str))
            
            # Expires At
            expires_str = session.expires_at.strftime("%Y-%m-%d %H:%M") if session.expires_at else ""
            item = QTableWidgetItem(expires_str)
            # Highlight expired sessions
            from datetime import datetime
            if session.expires_at and session.expires_at < datetime.now():
                item.setBackground(Qt.GlobalColor.lightCoral)
            self.table.setItem(row, 7, item)
    
    def filter_table(self):
        """Filter table based on search input and status filter"""
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
                active_item = self.table.item(row, 5)  # Active column
                if active_item:
                    if status_filter == "Active" and active_item.text() != "Yes":
                        should_show = False
                    elif status_filter == "Inactive" and active_item.text() != "No":
                        should_show = False
            
            self.table.setRowHidden(row, not should_show)
    
    def on_item_double_clicked(self, item):
        """Handle item double click"""
        row = item.row()
        session_id = int(self.table.item(row, 0).text())
        self.session_edit_requested.emit(session_id)
    
    def on_selection_changed(self):
        """Handle selection change"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            session_id = int(self.table.item(current_row, 0).text())
            self.session_selected.emit(session_id)
    
    def clean_expired_sessions(self):
        """Clean expired sessions from database"""
        try:
            reply = QMessageBox.question(
                self, 
                "Clean Expired Sessions", 
                "Are you sure you want to delete all expired sessions?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                with db_manager.get_session() as session:
                    from datetime import datetime
                    deleted_count = session.query(UserSession).filter(
                        UserSession.expires_at < datetime.now()
                    ).delete()
                    # Session commit is handled by the context manager
                
                QMessageBox.information(self, "Success", f"Deleted {deleted_count} expired sessions.")
                self.load_sessions()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to clean expired sessions:\n{str(e)}")
    
    def get_selected_session_id(self) -> Optional[int]:
        """Get the ID of currently selected session"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            return int(self.table.item(current_row, 0).text())
        return None
    
    def refresh_data(self):
        """Refresh the session data"""
        self.load_sessions()

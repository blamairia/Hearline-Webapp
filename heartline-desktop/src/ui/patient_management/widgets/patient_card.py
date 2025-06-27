"""
Patient Card Widget for Card-Based View

This widget displays patient information in a modern card format,
suitable for dashboard and overview displays.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QGridLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QTimer
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QBrush, QPen
from typing import List, Optional
from datetime import datetime

from src.models.complete_models import Patient
from src.ui.styles import AppColors


class PatientCard(QFrame):
    """Individual patient card widget"""
    
    clicked = pyqtSignal(int)  # Emitted when card is clicked
    edit_requested = pyqtSignal(int)  # Emitted when edit is requested
    view_requested = pyqtSignal(int)  # Emitted when view is requested
    
    def __init__(self, patient: Patient, parent=None):
        super().__init__(parent)
        self.patient = patient
        self.setup_ui()
        self.setup_styling()
    
    def setup_ui(self):
        """Setup the card UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Header with avatar and basic info
        header_layout = QHBoxLayout()
        
        # Avatar
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(50, 50)
        self.create_avatar()
        header_layout.addWidget(self.avatar_label)
        
        # Name and basic info
        info_layout = QVBoxLayout()
        
        # Full name
        full_name = f"{self.patient.first_name or ''} {self.patient.last_name or ''}".strip()
        self.name_label = QLabel(full_name)
        self.name_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.name_label.setStyleSheet(f"color: {AppColors.PRIMARY};")
        info_layout.addWidget(self.name_label)
        
        # Age and gender
        details = []
        if self.patient.age:
            details.append(f"Age: {self.patient.age}")
        if self.patient.gender:
            details.append(f"Gender: {self.patient.gender}")
        
        if details:
            self.details_label = QLabel(" • ".join(details))
            self.details_label.setFont(QFont("Segoe UI", 9))
            self.details_label.setStyleSheet(f"color: {AppColors.TEXT_SECONDARY};")
            info_layout.addWidget(self.details_label)
        
        header_layout.addLayout(info_layout)
        header_layout.addStretch()
        
        # Status indicator
        status = "Active" if getattr(self.patient, 'is_active', True) else "Inactive"
        self.status_label = QLabel(status)
        self.status_label.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        if status == "Active":
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #4caf50;
                    color: white;
                    padding: 2px 6px;
                    border-radius: 8px;
                }
            """)
        else:
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #f44336;
                    color: white;
                    padding: 2px 6px;
                    border-radius: 8px;
                }
            """)
        header_layout.addWidget(self.status_label)
        
        layout.addLayout(header_layout)
        
        # Contact information
        contact_layout = QVBoxLayout()
        
        if self.patient.phone:
            phone_label = QLabel(f"📞 {self.patient.phone}")
            phone_label.setFont(QFont("Segoe UI", 9))
            contact_layout.addWidget(phone_label)
        
        if self.patient.email:
            email_label = QLabel(f"📧 {self.patient.email}")
            email_label.setFont(QFont("Segoe UI", 9))
            email_label.setWordWrap(True)
            contact_layout.addWidget(email_label)
        
        layout.addLayout(contact_layout)
        
        # Medical highlights
        medical_layout = QVBoxLayout()
        
        if self.patient.insurance_provider:
            insurance_label = QLabel(f"🏥 {self.patient.insurance_provider}")
            insurance_label.setFont(QFont("Segoe UI", 9))
            insurance_label.setStyleSheet(f"color: {AppColors.SUCCESS};")
            medical_layout.addWidget(insurance_label)
        else:
            no_insurance_label = QLabel("🏥 No Insurance")
            no_insurance_label.setFont(QFont("Segoe UI", 9))
            no_insurance_label.setStyleSheet(f"color: {AppColors.WARNING};")
            medical_layout.addWidget(no_insurance_label)
        
        if self.patient.allergies:
            allergies_text = self.patient.allergies[:30] + "..." if len(self.patient.allergies) > 30 else self.patient.allergies
            allergies_label = QLabel(f"⚠️ Allergies: {allergies_text}")
            allergies_label.setFont(QFont("Segoe UI", 9))
            allergies_label.setStyleSheet(f"color: {AppColors.ERROR};")
            allergies_label.setWordWrap(True)
            medical_layout.addWidget(allergies_label)
        
        layout.addLayout(medical_layout)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.view_btn = QPushButton("👁️")
        self.view_btn.setFixedSize(30, 24)
        self.view_btn.setToolTip("View Details")
        self.view_btn.clicked.connect(lambda: self.view_requested.emit(self.patient.id))
        
        self.edit_btn = QPushButton("✏️")
        self.edit_btn.setFixedSize(30, 24)
        self.edit_btn.setToolTip("Edit Patient")
        self.edit_btn.clicked.connect(lambda: self.edit_requested.emit(self.patient.id))
        
        button_layout.addWidget(self.view_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addStretch()
        
        # Last visit info
        if self.patient.created_at:
            created_date = self.patient.created_at.strftime("%m/%d/%Y")
            created_label = QLabel(f"Created: {created_date}")
            created_label.setFont(QFont("Segoe UI", 8))
            created_label.setStyleSheet(f"color: {AppColors.TEXT_SECONDARY};")
            button_layout.addWidget(created_label)
        
        layout.addLayout(button_layout)
    
    def create_avatar(self):
        """Create patient avatar"""
        # Create a simple avatar with initials
        initials = ""
        if self.patient.first_name:
            initials += self.patient.first_name[0].upper()
        if self.patient.last_name:
            initials += self.patient.last_name[0].upper()
        
        if not initials:
            initials = "?"
        
        # Create pixmap
        pixmap = QPixmap(50, 50)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background circle
        color = QColor(AppColors.PRIMARY)
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(Qt.GlobalColor.transparent))
        painter.drawEllipse(0, 0, 50, 50)
        
        # Text
        painter.setPen(QPen(QColor("white")))
        painter.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        painter.drawText(0, 0, 50, 50, Qt.AlignmentFlag.AlignCenter, initials)
        
        painter.end()
        
        self.avatar_label.setPixmap(pixmap)
    
    def setup_styling(self):
        """Setup card styling"""
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {AppColors.BORDER};
                border-radius: 8px;
                padding: 4px;
            }}
            QFrame:hover {{
                border: 2px solid {AppColors.PRIMARY};
                background-color: #f8f9fa;
            }}
        """)
        
        # Set fixed size
        self.setFixedSize(280, 200)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    
    def mousePressEvent(self, event):
        """Handle mouse press event"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.patient.id)
        super().mousePressEvent(event)


class PatientCardWidget(QWidget):
    """Widget for displaying patients in card format"""
    
    # Signals
    patient_selected = pyqtSignal(int)
    patient_edit_requested = pyqtSignal(int)
    patient_view_requested = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.patients: List[Patient] = []
        self.cards: List[PatientCard] = []
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the widget UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("👥 Patients Cards")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {AppColors.PRIMARY}; margin: 10px;")
        layout.addWidget(title_label)
        
        # Scroll area for cards
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Cards container
        self.cards_container = QWidget()
        self.cards_layout = QGridLayout(self.cards_container)
        self.cards_layout.setSpacing(15)
        
        self.scroll_area.setWidget(self.cards_container)
        layout.addWidget(self.scroll_area)
        
        # Status label
        self.status_label = QLabel("No patients to display")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(f"color: {AppColors.TEXT_SECONDARY}; padding: 20px;")
        layout.addWidget(self.status_label)
    
    def set_patients(self, patients: List[Patient]):
        """Set the patients to display"""
        self.patients = patients
        self.create_cards()
    
    def create_cards(self):
        """Create patient cards"""
        # Clear existing cards
        self.clear_cards()
        
        if not self.patients:
            self.status_label.setText("No patients to display")
            self.status_label.show()
            return
        
        self.status_label.hide()
        
        # Calculate columns based on available width
        card_width = 300  # Including spacing
        available_width = self.scroll_area.viewport().width()
        columns = max(1, available_width // card_width)
        
        # Create cards
        row = 0
        col = 0
        
        for patient in self.patients:
            card = PatientCard(patient)
            card.clicked.connect(self.patient_selected.emit)
            card.edit_requested.connect(self.patient_edit_requested.emit)
            card.view_requested.connect(self.patient_view_requested.emit)
            
            self.cards_layout.addWidget(card, row, col)
            self.cards.append(card)
            
            col += 1
            if col >= columns:
                col = 0
                row += 1
        
        # Add stretch to fill remaining space
        self.cards_layout.setRowStretch(row + 1, 1)
        self.cards_layout.setColumnStretch(columns, 1)
        
        # Update status
        self.status_label.setText(f"Displaying {len(self.patients)} patients")
    
    def clear_cards(self):
        """Clear all cards"""
        for card in self.cards:
            card.deleteLater()
        self.cards.clear()
        
        # Clear layout
        while self.cards_layout.count():
            child = self.cards_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def resizeEvent(self, event):
        """Handle resize event to adjust card layout"""
        super().resizeEvent(event)
        if self.patients:
            # Recreate cards with new column count
            QTimer.singleShot(100, self.create_cards)  # Delay to ensure proper sizing
    
    def refresh(self):
        """Refresh the cards"""
        self.create_cards()

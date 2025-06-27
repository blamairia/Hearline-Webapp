"""
ECG Analysis Widget - Placeholder
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ECGAnalysisWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("ECG Analysis - Under Development"))

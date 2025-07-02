"""
Global color palette and styling constants for Heartline Desktop Application

This module provides a centralized color management system to ensure consistent
styling across all components of the application.
"""

from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

class AppColors:
    """Main application color palette"""
    
    # Primary Colors
    PRIMARY = "#2196F3"        # Blue
    PRIMARY_DARK = "#1976D2"   # Darker blue
    PRIMARY_LIGHT = "#E3F2FD"  # Light blue
    
    # Secondary Colors
    SECONDARY = "#FF9800"      # Orange
    SECONDARY_DARK = "#F57C00" # Dark orange
    SECONDARY_LIGHT = "#FFF3E0" # Light orange
    
    # Background Colors
    BACKGROUND = "#FFFFFF"     # White
    BACKGROUND_SECONDARY = "#F5F5F5"  # Light gray
    BACKGROUND_ACCENT = "#FAFAFA"     # Very light gray
    SURFACE = "#FFFFFF"        # Surface color (same as background)
    CARD_BACKGROUND = "#FFFFFF"       # Card background color
    
    # Text Colors
    TEXT = "#212121"           # Primary text color (same as TEXT_PRIMARY)
    TEXT_PRIMARY = "#212121"    # Dark gray/black
    TEXT_SECONDARY = "#757575"  # Medium gray
    TEXT_DISABLED = "#BDBDBD"   # Light gray
    TEXT_ON_PRIMARY = "#FFFFFF" # White text on primary color
    
    # Status Colors
    SUCCESS = "#4CAF50"        # Green
    SUCCESS_LIGHT = "#E8F5E8"  # Light green
    WARNING = "#FF9800"        # Orange
    WARNING_LIGHT = "#FFF3E0"  # Light orange
    ERROR = "#F44336"          # Red
    ERROR_LIGHT = "#FFEBEE"    # Light red
    INFO = "#2196F3"           # Blue
    INFO_LIGHT = "#E3F2FD"     # Light blue
    
    # Border Colors
    BORDER = "#E0E0E0"         # Light gray
    BORDER_FOCUS = "#2196F3"   # Blue
    BORDER_ERROR = "#F44336"   # Red
    
    # Table Colors
    TABLE_HEADER = "#2196F3"        # Blue header
    TABLE_ALTERNATE = "#F5F5F5"     # Alternate row color
    TABLE_SELECTION = "#E3F2FD"     # Selection background
    TABLE_HOVER = "#F0F0F0"         # Hover color
    
    # Button Colors
    BUTTON_PRIMARY = "#2196F3"      # Primary button
    BUTTON_PRIMARY_HOVER = "#1976D2" # Primary button hover
    BUTTON_SECONDARY = "#757575"    # Secondary button
    BUTTON_SECONDARY_HOVER = "#616161" # Secondary button hover
    BUTTON_SUCCESS = "#4CAF50"      # Success button
    BUTTON_WARNING = "#FF9800"      # Warning button
    BUTTON_DANGER = "#F44336"       # Danger button
    
    # Navigation Colors
    NAV_BACKGROUND = "#FFFFFF"      # Navigation background
    NAV_SELECTED = "#E3F2FD"        # Selected nav item
    NAV_HOVER = "#F5F5F5"           # Nav item hover
    
    # Additional UI Colors
    HOVER = "#F0F7FF"              # Light blue hover
    SELECTED = "#E3F2FD"           # Light blue selection
    DISABLED = "#F5F5F5"           # Disabled background
    PRIMARY_HOVER = "#1976D2"      # Primary hover (same as PRIMARY_DARK)
    PRIMARY_PRESSED = "#0D47A1"    # Primary pressed state
    
    # Form Colors
    INPUT_BACKGROUND = "#FFFFFF"    # Input field background
    INPUT_BORDER = "#E0E0E0"        # Input field border
    INPUT_FOCUS = "#2196F3"         # Input field focus
    
    @classmethod
    def get_qcolor(cls, color_hex: str) -> QColor:
        """Convert hex color to QColor"""
        return QColor(color_hex)
    
    @classmethod
    def get_status_color(cls, status: str) -> str:
        """Get color for specific status"""
        status_map = {
            'active': cls.SUCCESS,
            'inactive': cls.TEXT_DISABLED,
            'pending': cls.WARNING,
            'error': cls.ERROR,
            'completed': cls.SUCCESS,
            'cancelled': cls.ERROR,
            'scheduled': cls.INFO,
            'waiting': cls.WARNING,
            'called': cls.INFO,
            'in_progress': cls.INFO,
        }
        return status_map.get(status.lower(), cls.TEXT_SECONDARY)

class AppStyles:
    """Centralized styling templates"""
    
    # Main application style with all common widgets
    APP_STYLE = f"""
        QWidget {{
            background-color: {AppColors.BACKGROUND};
            color: {AppColors.TEXT_PRIMARY};
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        
        QLineEdit {{
            background-color: {AppColors.INPUT_BACKGROUND};
            border: 1px solid {AppColors.INPUT_BORDER};
            border-radius: 4px;
            padding: 8px;
            color: {AppColors.TEXT_PRIMARY};
            font-size: 12px;
        }}
        QLineEdit:focus {{
            border-color: {AppColors.INPUT_FOCUS};
        }}
        
        QTextEdit {{
            background-color: {AppColors.INPUT_BACKGROUND};
            border: 1px solid {AppColors.INPUT_BORDER};
            border-radius: 4px;
            padding: 8px;
            color: {AppColors.TEXT_PRIMARY};
            font-size: 12px;
        }}
        QTextEdit:focus {{
            border-color: {AppColors.INPUT_FOCUS};
        }}
        
        QComboBox {{
            background-color: {AppColors.INPUT_BACKGROUND};
            border: 1px solid {AppColors.INPUT_BORDER};
            border-radius: 4px;
            padding: 8px;
            color: {AppColors.TEXT_PRIMARY};
            font-size: 12px;
        }}
        QComboBox:focus {{
            border-color: {AppColors.INPUT_FOCUS};
        }}
        QComboBox::drop-down {{
            border: none;
            background-color: {AppColors.PRIMARY};
            border-radius: 2px;
        }}
        QComboBox::down-arrow {{
            border: none;
            background-color: transparent;
        }}
        QComboBox QAbstractItemView {{
            background-color: {AppColors.INPUT_BACKGROUND};
            border: 1px solid {AppColors.INPUT_BORDER};
            color: {AppColors.TEXT_PRIMARY};
            selection-background-color: {AppColors.PRIMARY_LIGHT};
            selection-color: {AppColors.TEXT_PRIMARY};
        }}
        
        QSpinBox, QDateEdit {{
            background-color: {AppColors.INPUT_BACKGROUND};
            border: 1px solid {AppColors.INPUT_BORDER};
            border-radius: 4px;
            padding: 8px;
            color: {AppColors.TEXT_PRIMARY};
            font-size: 12px;
        }}
        
        QGroupBox {{
            font-weight: bold;
            color: {AppColors.TEXT_PRIMARY};
            border: 2px solid {AppColors.BORDER};
            border-radius: 4px;
            margin-top: 1ex;
            background: transparent;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
            color: {AppColors.PRIMARY};
        }}
        
        QTabWidget::pane {{
            border: 1px solid {AppColors.BORDER};
            background: {AppColors.BACKGROUND};
        }}
        QTabBar::tab {{
            background: {AppColors.BACKGROUND_SECONDARY};
            color: {AppColors.TEXT_PRIMARY};
            padding: 8px 12px;
            margin: 1px;
        }}
        QTabBar::tab:selected {{
            background: {AppColors.PRIMARY};
            color: {AppColors.TEXT_ON_PRIMARY};
        }}
        
        QScrollArea {{
            background: {AppColors.BACKGROUND};
            border: none;
        }}
        
        QFrame {{
            background: {AppColors.BACKGROUND};
            border: none;
        }}
    """
    
    # Dialog specific style
    DIALOG_STYLE = f"""
        QDialog {{
            background-color: {AppColors.BACKGROUND};
            color: {AppColors.TEXT_PRIMARY};
        }}
        {APP_STYLE}
    """
    
    # Button style constants
    PRIMARY_BUTTON_STYLE = f"""
        QPushButton {{
            background-color: {AppColors.BUTTON_PRIMARY};
            color: {AppColors.TEXT_ON_PRIMARY};
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 12px;
        }}
        QPushButton:hover {{
            background-color: {AppColors.BUTTON_PRIMARY_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {AppColors.PRIMARY_DARK};
        }}
        QPushButton:disabled {{
            background-color: {AppColors.TEXT_DISABLED};
            color: {AppColors.BACKGROUND};
        }}
    """
    
    SECONDARY_BUTTON_STYLE = f"""
        QPushButton {{
            background-color: {AppColors.BUTTON_SECONDARY};
            color: {AppColors.TEXT_ON_PRIMARY};
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 12px;
        }}
        QPushButton:hover {{
            background-color: {AppColors.BUTTON_SECONDARY_HOVER};
        }}
    """
    
    SUCCESS_BUTTON_STYLE = f"""
        QPushButton {{
            background-color: {AppColors.BUTTON_SUCCESS};
            color: {AppColors.TEXT_ON_PRIMARY};
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 12px;
        }}
        QPushButton:hover {{
            background-color: #45a049;
        }}
    """
    
    WARNING_BUTTON_STYLE = f"""
        QPushButton {{
            background-color: {AppColors.BUTTON_WARNING};
            color: {AppColors.TEXT_ON_PRIMARY};
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 12px;
        }}
        QPushButton:hover {{
            background-color: #e68900;
        }}
    """
    
    DANGER_BUTTON_STYLE = f"""
        QPushButton {{
            background-color: {AppColors.BUTTON_DANGER};
            color: {AppColors.TEXT_ON_PRIMARY};
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 12px;
        }}
        QPushButton:hover {{
            background-color: #da190b;
        }}
    """

    @staticmethod
    def get_table_style() -> str:
        """Get standard table widget styling with improved contrast"""
        return f"""
            QTableWidget {{
                background-color: {AppColors.BACKGROUND};
                alternate-background-color: {AppColors.TABLE_ALTERNATE};
                selection-background-color: {AppColors.PRIMARY_LIGHT};
                gridline-color: {AppColors.BORDER};
                color: {AppColors.TEXT_PRIMARY};
                border: 1px solid {AppColors.BORDER};
                border-radius: 4px;
            }}
            QTableWidget::item {{
                padding: 10px 8px;
                border-bottom: 1px solid {AppColors.BORDER};
                color: {AppColors.TEXT_PRIMARY};
                background-color: transparent;
            }}
            QTableWidget::item:hover {{
                background-color: {AppColors.HOVER};
                color: {AppColors.TEXT_PRIMARY};
            }}
            QTableWidget::item:selected {{
                background-color: {AppColors.PRIMARY_LIGHT};
                color: {AppColors.TEXT_PRIMARY};
                font-weight: bold;
            }}
            QTableWidget::item:selected:hover {{
                background-color: {AppColors.PRIMARY_LIGHT};
                color: {AppColors.TEXT_PRIMARY};
            }}
            QHeaderView::section {{
                background-color: {AppColors.TABLE_HEADER};
                color: {AppColors.TEXT_ON_PRIMARY};
                padding: 12px 8px;
                border: none;
                border-right: 1px solid {AppColors.PRIMARY_DARK};
                font-weight: bold;
                font-size: 12px;
                text-align: center;
            }}
            QHeaderView::section:hover {{
                background-color: {AppColors.PRIMARY_DARK};
            }}
            QHeaderView::section:last {{
                border-right: none;
            }}
        """
    
    @staticmethod
    def get_button_style(button_type: str = "primary") -> str:
        """Get button styling based on type"""
        styles = {
            "primary": f"""
                QPushButton {{
                    background-color: {AppColors.BUTTON_PRIMARY};
                    color: {AppColors.TEXT_ON_PRIMARY};
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: {AppColors.BUTTON_PRIMARY_HOVER};
                }}
                QPushButton:pressed {{
                    background-color: {AppColors.PRIMARY_DARK};
                }}
                QPushButton:disabled {{
                    background-color: {AppColors.TEXT_DISABLED};
                    color: {AppColors.BACKGROUND};
                }}
            """,
            "secondary": f"""
                QPushButton {{
                    background-color: {AppColors.BUTTON_SECONDARY};
                    color: {AppColors.TEXT_ON_PRIMARY};
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: {AppColors.BUTTON_SECONDARY_HOVER};
                }}
            """,
            "success": f"""
                QPushButton {{
                    background-color: {AppColors.BUTTON_SUCCESS};
                    color: {AppColors.TEXT_ON_PRIMARY};
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: #45a049;
                }}
            """,
            "warning": f"""
                QPushButton {{
                    background-color: {AppColors.BUTTON_WARNING};
                    color: {AppColors.TEXT_ON_PRIMARY};
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: #e68900;
                }}
            """,
            "danger": f"""
                QPushButton {{
                    background-color: {AppColors.BUTTON_DANGER};
                    color: {AppColors.TEXT_ON_PRIMARY};
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: #da190b;
                }}
            """
        }
        return styles.get(button_type, styles["primary"])
    
    @staticmethod
    def get_input_style() -> str:
        """Get input field styling"""
        return f"""
            QLineEdit, QComboBox {{
                background-color: {AppColors.INPUT_BACKGROUND};
                border: 2px solid {AppColors.INPUT_BORDER};
                border-radius: 4px;
                padding: 8px;
                font-size: 12px;
                color: {AppColors.TEXT_PRIMARY};
            }}
            QLineEdit:focus, QComboBox:focus {{
                border-color: {AppColors.INPUT_FOCUS};
            }}
            QComboBox::drop-down {{
                border: none;
                background-color: {AppColors.PRIMARY};
                border-radius: 2px;
            }}
            QComboBox::down-arrow {{
                border: none;
                background-color: transparent;
            }}
        """
    
    @staticmethod
    def get_navigation_style() -> str:
        """Get navigation panel styling"""
        return f"""
            QWidget#navigation {{
                background-color: {AppColors.NAV_BACKGROUND};
                border-right: 1px solid {AppColors.BORDER};
            }}
            QPushButton#nav_button {{
                background-color: transparent;
                border: none;
                padding: 12px 16px;
                text-align: left;
                font-size: 13px;
                color: {AppColors.TEXT_PRIMARY};
                border-radius: 0px;
            }}
            QPushButton#nav_button:hover {{
                background-color: {AppColors.NAV_HOVER};
            }}
            QPushButton#nav_button:checked {{
                background-color: {AppColors.NAV_SELECTED};
                color: {AppColors.PRIMARY};
                font-weight: bold;
                border-left: 3px solid {AppColors.PRIMARY};
            }}
        """
    
    @staticmethod
    def get_title_style(size: str = "large") -> str:
        """Get title styling"""
        sizes = {
            "large": "18px",
            "medium": "16px",
            "small": "14px"
        }
        return f"""
            color: {AppColors.PRIMARY};
            font-size: {sizes.get(size, sizes['large'])};
            font-weight: bold;
            margin: 10px;
        """
    
    @staticmethod
    def get_status_label_style() -> str:
        """Get status label styling"""
        return f"""
            color: {AppColors.TEXT_SECONDARY};
            font-size: 12px;
            margin: 5px;
            padding: 4px 8px;
            background-color: {AppColors.BACKGROUND_SECONDARY};
            border-radius: 4px;
        """
    
    @staticmethod
    def get_frame_style() -> str:
        """Get frame/container styling"""
        return f"""
            QFrame {{
                background-color: {AppColors.BACKGROUND};
                border: 1px solid {AppColors.BORDER};
                border-radius: 4px;
                padding: 8px;
            }}
        """

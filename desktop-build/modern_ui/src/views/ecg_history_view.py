"""
ECG History View - Placeholder
"""

import customtkinter as ctk

class ECGHistoryView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.app = app
        
        label = ctk.CTkLabel(
            self,
            text="🚧 ECG History Coming Soon",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        label.pack(expand=True)

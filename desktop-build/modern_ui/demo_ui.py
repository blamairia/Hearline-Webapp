"""
HeartLine Modern UI Demo
Showcases the modern desktop UI concept using standard tkinter

This demonstrates what the full CustomTkinter version would look like
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
from datetime import datetime
from pathlib import Path

class HeartLineModernUIDemo:
    """
    Demo version of the HeartLine desktop application
    Shows the modern UI concept using standard tkinter
    """
    
    def __init__(self):
        # Application configuration
        self.app_title = "HeartLine Medical Clinic - Modern UI Demo"
        self.current_view = "dashboard"
        
        # Color scheme matching the Flask app
        self.colors = {
            'primary': '#0074d9',
            'primary_dark': '#0056b3', 
            'secondary': '#00b4ff',
            'success': '#28a745',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'background': '#f8f9fa',
            'white': '#ffffff',
            'text_dark': '#212529',
            'text_light': '#6c757d'
        }
        
        # Initialize the main window
        self.setup_main_window()
        self.setup_layout()
        self.show_dashboard()
        
    def setup_main_window(self):
        """Initialize the main application window"""
        self.root = tk.Tk()
        self.root.title(self.app_title)
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        self.root.configure(bg=self.colors['background'])
        
        # Center window
        self.center_window()
        
        # Configure style
        self.setup_styles()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = 1400
        height = 900
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_styles(self):
        """Configure ttk styles"""
        self.style = ttk.Style()
        
        # Configure button styles
        self.style.configure('Primary.TButton',
                           background=self.colors['primary'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           font=('Segoe UI', 10, 'bold'))
        
        self.style.configure('Success.TButton',
                           background=self.colors['success'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           font=('Segoe UI', 10, 'bold'))
                           
        # Configure label styles
        self.style.configure('Title.TLabel',
                           background=self.colors['background'],
                           foreground=self.colors['text_dark'],
                           font=('Segoe UI', 24, 'bold'))
                           
        self.style.configure('Subtitle.TLabel',
                           background=self.colors['background'],
                           foreground=self.colors['text_light'],
                           font=('Segoe UI', 12))
                           
        self.style.configure('Sidebar.TLabel',
                           background=self.colors['primary'],
                           foreground='white',
                           font=('Segoe UI', 12))
    
    def setup_layout(self):
        """Create the main layout with sidebar and content area"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.setup_sidebar(main_frame)
        
        # Main content area
        self.setup_main_content(main_frame)
        
    def setup_sidebar(self, parent):
        """Create the sidebar navigation"""
        sidebar = tk.Frame(parent, bg=self.colors['primary'], width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Sidebar header
        header_frame = tk.Frame(sidebar, bg=self.colors['primary'])
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Logo placeholder
        logo_frame = tk.Frame(header_frame, bg='white', width=80, height=80)
        logo_frame.pack(pady=(0, 10))
        logo_frame.pack_propagate(False)
        
        logo_label = tk.Label(logo_frame, text="❤️", font=('Segoe UI', 24), 
                             bg='white', fg=self.colors['primary'])
        logo_label.pack(expand=True)
        
        # App title
        title_label = tk.Label(header_frame, text="HeartLine", 
                              font=('Segoe UI', 18, 'bold'),
                              bg=self.colors['primary'], fg='white')
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Medical Clinic",
                                 font=('Segoe UI', 12),
                                 bg=self.colors['primary'], fg='white')
        subtitle_label.pack()
        
        # Navigation menu
        nav_frame = tk.Frame(sidebar, bg=self.colors['primary'])
        nav_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Navigation buttons
        nav_items = [
            ("🏠  Dashboard", self.show_dashboard),
            ("👤  New Patient", self.show_new_patient),
            ("📋  New Visit", self.show_new_visit),
            ("👥  Patients", self.show_patients),
            ("📊  Visits", self.show_visits),
            ("📅  Appointments", self.show_appointments),
            ("💓  ECG History", self.show_ecg_history),
        ]
        
        self.nav_buttons = []
        for text, command in nav_items:
            btn = tk.Button(nav_frame, text=text, font=('Segoe UI', 12),
                           bg=self.colors['primary'], fg='white',
                           relief=tk.FLAT, anchor='w', padx=20, pady=10,
                           command=command, cursor='hand2')
            btn.pack(fill=tk.X, pady=2)
            self.nav_buttons.append(btn)
            
            # Hover effects
            def on_enter(e, button=btn):
                button.config(bg=self.colors['primary_dark'])
            def on_leave(e, button=btn):
                if button['text'].split()[0] + "  " + button['text'].split()[1] != self.get_current_nav_text():
                    button.config(bg=self.colors['primary'])
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        
        # Set dashboard as active
        self.set_active_nav(0)
        
        # Footer
        footer_frame = tk.Frame(sidebar, bg=self.colors['primary_dark'], height=60)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        user_label = tk.Label(footer_frame, text="👨‍⚕️ Dr. Admin",
                             font=('Segoe UI', 11), bg=self.colors['primary_dark'], fg='white')
        user_label.pack(expand=True)
    
    def setup_main_content(self, parent):
        """Create the main content area"""
        # Main content frame
        self.main_content = tk.Frame(parent, bg=self.colors['background'])
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Top bar
        top_bar = tk.Frame(self.main_content, bg='white', height=60)
        top_bar.pack(fill=tk.X, padx=0, pady=(0, 1))
        top_bar.pack_propagate(False)
        
        # Page title
        self.page_title = tk.Label(top_bar, text="Dashboard", 
                                  font=('Segoe UI', 20, 'bold'),
                                  bg='white', fg=self.colors['text_dark'])
        self.page_title.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Action buttons
        action_frame = tk.Frame(top_bar, bg='white')
        action_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        new_patient_btn = tk.Button(action_frame, text="+ New Patient",
                                   font=('Segoe UI', 10, 'bold'),
                                   bg=self.colors['primary'], fg='white',
                                   relief=tk.FLAT, padx=15, pady=8,
                                   command=self.show_new_patient, cursor='hand2')
        new_patient_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        new_visit_btn = tk.Button(action_frame, text="+ New Visit",
                                 font=('Segoe UI', 10, 'bold'),
                                 bg=self.colors['success'], fg='white',
                                 relief=tk.FLAT, padx=15, pady=8,
                                 command=self.show_new_visit, cursor='hand2')
        new_visit_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Content container
        self.content_container = tk.Frame(self.main_content, bg=self.colors['background'])
        self.content_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Status bar
        status_bar = tk.Frame(self.main_content, bg=self.colors['text_light'], height=25)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        status_bar.pack_propagate(False)
        
        status_label = tk.Label(status_bar, text="Ready | Modern Desktop UI Demo",
                               font=('Segoe UI', 9), bg=self.colors['text_light'], fg='white')
        status_label.pack(side=tk.LEFT, padx=10, pady=2)
        
        time_label = tk.Label(status_bar, text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                             font=('Segoe UI', 9), bg=self.colors['text_light'], fg='white')
        time_label.pack(side=tk.RIGHT, padx=10, pady=2)
    
    def clear_content(self):
        """Clear the content container"""
        for widget in self.content_container.winfo_children():
            widget.destroy()
    
    def set_active_nav(self, index):
        """Set active navigation button"""
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.config(bg='white', fg=self.colors['primary'])
            else:
                btn.config(bg=self.colors['primary'], fg='white')
    
    def get_current_nav_text(self):
        """Get current navigation text for active state"""
        nav_texts = ["🏠  Dashboard", "👤  New Patient", "📋  New Visit", 
                    "👥  Patients", "📊  Visits", "📅  Appointments", "💓  ECG History"]
        if self.current_view == "dashboard":
            return nav_texts[0]
        return ""
    
    def show_dashboard(self):
        """Show dashboard view"""
        self.current_view = "dashboard"
        self.clear_content()
        self.page_title.config(text="📊 Dashboard")
        self.set_active_nav(0)
        
        # Create dashboard content
        welcome_frame = tk.Frame(self.content_container, bg='white', relief=tk.FLAT, bd=1)
        welcome_frame.pack(fill=tk.X, pady=(0, 20))
        
        welcome_label = tk.Label(welcome_frame, text="👋 Welcome back, Dr. Admin!",
                                font=('Segoe UI', 20, 'bold'),
                                bg='white', fg=self.colors['text_dark'])
        welcome_label.pack(pady=20)
        
        date_label = tk.Label(welcome_frame, text=datetime.now().strftime("%A, %B %d, %Y"),
                             font=('Segoe UI', 12),
                             bg='white', fg=self.colors['text_light'])
        date_label.pack(pady=(0, 20))
        
        # Statistics cards
        stats_frame = tk.Frame(self.content_container, bg=self.colors['background'])
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        stats_data = [
            ("👥 Total Patients", "1,247", self.colors['primary']),
            ("📋 Today's Visits", "23", self.colors['success']),
            ("📅 Appointments", "18", self.colors['warning']),
            ("💓 ECG Analyses", "156", self.colors['danger'])
        ]
        
        for i, (title, value, color) in enumerate(stats_data):
            card = tk.Frame(stats_frame, bg='white', relief=tk.FLAT, bd=1)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
            title_label = tk.Label(card, text=title, font=('Segoe UI', 12),
                                  bg='white', fg=color)
            title_label.pack(pady=(15, 5))
            
            value_label = tk.Label(card, text=value, font=('Segoe UI', 24, 'bold'),
                                  bg='white', fg=self.colors['text_dark'])
            value_label.pack()
            
            change_label = tk.Label(card, text="+12%", font=('Segoe UI', 10),
                                   bg='white', fg=self.colors['success'])
            change_label.pack(pady=(5, 15))
        
        # Quick actions
        actions_frame = tk.Frame(self.content_container, bg='white', relief=tk.FLAT, bd=1)
        actions_frame.pack(fill=tk.X, pady=(20, 0))
        
        actions_title = tk.Label(actions_frame, text="⚡ Quick Actions",
                                font=('Segoe UI', 16, 'bold'),
                                bg='white', fg=self.colors['text_dark'])
        actions_title.pack(pady=(20, 15))
        
        actions_grid = tk.Frame(actions_frame, bg='white')
        actions_grid.pack(pady=(0, 20))
        
        quick_actions = [
            ("👤 New Patient", self.show_new_patient, self.colors['primary']),
            ("📅 Schedule", self.show_appointments, self.colors['success']),
            ("💓 Upload ECG", self.show_new_visit, self.colors['danger']),
            ("📊 Reports", self.show_reports, self.colors['warning'])
        ]
        
        for i, (text, command, color) in enumerate(quick_actions):
            btn = tk.Button(actions_grid, text=text,
                           font=('Segoe UI', 11, 'bold'),
                           bg=color, fg='white', relief=tk.FLAT,
                           padx=20, pady=15, command=command, cursor='hand2')
            btn.pack(side=tk.LEFT, padx=10)
    
    def show_new_patient(self):
        """Show new patient form"""
        self.current_view = "new_patient"
        self.clear_content()
        self.page_title.config(text="👤 New Patient")
        self.set_active_nav(1)
        
        form_frame = tk.Frame(self.content_container, bg='white', relief=tk.FLAT, bd=1)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(form_frame, text="👤 Create New Patient",
                              font=('Segoe UI', 18, 'bold'),
                              bg='white', fg=self.colors['text_dark'])
        title_label.pack(pady=20)
        
        # Demo form fields
        fields_frame = tk.Frame(form_frame, bg='white')
        fields_frame.pack(pady=20)
        
        # First Name
        tk.Label(fields_frame, text="First Name *", font=('Segoe UI', 10, 'bold'),
                bg='white', fg=self.colors['text_dark']).grid(row=0, column=0, sticky='w', padx=10, pady=5)
        tk.Entry(fields_frame, font=('Segoe UI', 10), width=25).grid(row=1, column=0, padx=10, pady=5)
        
        # Last Name
        tk.Label(fields_frame, text="Last Name *", font=('Segoe UI', 10, 'bold'),
                bg='white', fg=self.colors['text_dark']).grid(row=0, column=1, sticky='w', padx=10, pady=5)
        tk.Entry(fields_frame, font=('Segoe UI', 10), width=25).grid(row=1, column=1, padx=10, pady=5)
        
        # Date of Birth
        tk.Label(fields_frame, text="Date of Birth *", font=('Segoe UI', 10, 'bold'),
                bg='white', fg=self.colors['text_dark']).grid(row=2, column=0, sticky='w', padx=10, pady=5)
        tk.Entry(fields_frame, font=('Segoe UI', 10), width=25).grid(row=3, column=0, padx=10, pady=5)
        
        # Phone
        tk.Label(fields_frame, text="Phone Number *", font=('Segoe UI', 10, 'bold'),
                bg='white', fg=self.colors['text_dark']).grid(row=2, column=1, sticky='w', padx=10, pady=5)
        tk.Entry(fields_frame, font=('Segoe UI', 10), width=25).grid(row=3, column=1, padx=10, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg='white')
        btn_frame.pack(pady=20)
        
        save_btn = tk.Button(btn_frame, text="💾 Save Patient",
                            font=('Segoe UI', 11, 'bold'),
                            bg=self.colors['primary'], fg='white',
                            relief=tk.FLAT, padx=20, pady=10,
                            command=self.save_demo_patient, cursor='hand2')
        save_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = tk.Button(btn_frame, text="Cancel",
                              font=('Segoe UI', 11),
                              bg=self.colors['text_light'], fg='white',
                              relief=tk.FLAT, padx=20, pady=10,
                              command=self.show_dashboard, cursor='hand2')
        cancel_btn.pack(side=tk.LEFT, padx=10)
    
    def show_new_visit(self):
        """Show new visit form"""
        self.current_view = "new_visit"
        self.clear_content()
        self.page_title.config(text="📋 New Visit")
        self.set_active_nav(2)
        
        demo_label = tk.Label(self.content_container, text="🚧 New Visit Form\\n\\nComing Soon!",
                             font=('Segoe UI', 24, 'bold'),
                             bg=self.colors['background'], fg=self.colors['text_dark'])
        demo_label.pack(expand=True)
    
    def show_patients(self):
        """Show patients table"""
        self.current_view = "patients"
        self.clear_content()
        self.page_title.config(text="👥 Patients")
        self.set_active_nav(3)
        
        # Table frame
        table_frame = tk.Frame(self.content_container, bg='white', relief=tk.FLAT, bd=1)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Table title
        title_label = tk.Label(table_frame, text="👥 Patients Database",
                              font=('Segoe UI', 16, 'bold'),
                              bg='white', fg=self.colors['text_dark'])
        title_label.pack(pady=15)
        
        # Demo table with Treeview
        tree_frame = tk.Frame(table_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        columns = ("ID", "Name", "Age", "Gender", "Phone", "Last Visit")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        
        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        # Sample data
        sample_patients = [
            (1, "John Smith", 45, "Male", "+1-555-0123", "2024-07-10"),
            (2, "Sarah Johnson", 32, "Female", "+1-555-0124", "2024-07-09"),
            (3, "Michael Brown", 67, "Male", "+1-555-0125", "2024-07-08"),
            (4, "Emily Davis", 28, "Female", "+1-555-0126", "2024-07-07"),
            (5, "Robert Wilson", 55, "Male", "+1-555-0127", "2024-07-05")
        ]
        
        for patient in sample_patients:
            tree.insert("", "end", values=patient)
        
        tree.pack(fill=tk.BOTH, expand=True)
    
    def show_visits(self):
        """Show visits table"""
        self.current_view = "visits"
        self.clear_content()
        self.page_title.config(text="📊 Visits")
        self.set_active_nav(4)
        
        demo_label = tk.Label(self.content_container, text="🚧 Visits Table\\n\\nComing Soon!",
                             font=('Segoe UI', 24, 'bold'),
                             bg=self.colors['background'], fg=self.colors['text_dark'])
        demo_label.pack(expand=True)
    
    def show_appointments(self):
        """Show appointments table"""
        self.current_view = "appointments"
        self.clear_content()
        self.page_title.config(text="📅 Appointments")
        self.set_active_nav(5)
        
        demo_label = tk.Label(self.content_container, text="🚧 Appointments Table\\n\\nComing Soon!",
                             font=('Segoe UI', 24, 'bold'),
                             bg=self.colors['background'], fg=self.colors['text_dark'])
        demo_label.pack(expand=True)
    
    def show_ecg_history(self):
        """Show ECG history"""
        self.current_view = "ecg_history"
        self.clear_content()
        self.page_title.config(text="💓 ECG History")
        self.set_active_nav(6)
        
        demo_label = tk.Label(self.content_container, text="🚧 ECG History\\n\\nComing Soon!",
                             font=('Segoe UI', 24, 'bold'),
                             bg=self.colors['background'], fg=self.colors['text_dark'])
        demo_label.pack(expand=True)
    
    def show_reports(self):
        """Show reports"""
        messagebox.showinfo("Reports", "Reports functionality coming soon!")
    
    def save_demo_patient(self):
        """Save demo patient"""
        messagebox.showinfo("Success", "Demo patient saved successfully!\\n\\nIn the full version, this would save to the database.")
        self.show_patients()
    
    def run(self):
        """Start the application"""
        print("🚀 Starting HeartLine Modern UI Demo...")
        print("📱 Framework: Standard Tkinter")
        print("🎨 Theme: Modern Medical Design")
        print("✨ Features: Responsive Layout, Professional UI")
        print("💡 This demo shows what the full CustomTkinter version will look like")
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = HeartLineModernUIDemo()
        app.run()
    except Exception as e:
        print(f"Error running demo: {e}")
        input("Press Enter to exit...")

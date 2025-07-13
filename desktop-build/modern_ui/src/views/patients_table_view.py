"""
Patients Table View for HeartLine Desktop Application
Modern data table with search, filtering, and actions
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import threading

class PatientsTableView(ctk.CTkFrame):
    """
    Modern patients table with search, filter, and action capabilities
    """
    
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.app = app
        self.patients_data = []
        self.filtered_data = []
        self.setup_table_view()
        self.load_sample_data()
    
    def setup_table_view(self):
        """Create the complete table view layout"""
        # Configure grid weights
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Table header with search and filters
        self.create_table_header()
        
        # Table controls (search, filter, actions)
        self.create_table_controls()
        
        # Main data table
        self.create_data_table()
        
        # Table pagination
        self.create_pagination()
    
    def create_table_header(self):
        """Create the table header with title and quick actions"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title and stats
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="👥 Patients Database",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.app.colors['text_dark']
        )
        title_label.pack(side="left")
        
        # Patient count badge
        count_badge = ctk.CTkFrame(
            title_frame,
            corner_radius=15,
            fg_color=self.app.colors['primary']
        )
        count_badge.pack(side="left", padx=(15, 0))
        
        count_label = ctk.CTkLabel(
            count_badge,
            text="1,247 Total",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.app.colors['white']
        )
        count_label.pack(padx=12, pady=6)
        
        # Action buttons
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=2, sticky="e")
        
        # Export button
        export_btn = ctk.CTkButton(
            actions_frame,
            text="📊 Export",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=100,
            height=35,
            corner_radius=8,
            fg_color=self.app.colors['success'],
            hover_color="#218838",
            command=self.export_data
        )
        export_btn.pack(side="right", padx=(5, 0))
        
        # Add patient button
        add_btn = ctk.CTkButton(
            actions_frame,
            text="➕ New Patient",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=120,
            height=35,
            corner_radius=8,
            fg_color=self.app.colors['primary'],
            hover_color=self.app.colors['primary_dark'],
            command=self.app.show_new_patient
        )
        add_btn.pack(side="right", padx=(5, 0))
    
    def create_table_controls(self):
        """Create search and filter controls"""
        controls_frame = ctk.CTkFrame(
            self,
            corner_radius=10,
            fg_color=self.app.colors['white']
        )
        controls_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        controls_frame.grid_columnconfigure(0, weight=1)
        
        # Controls content
        controls_content = ctk.CTkFrame(controls_frame, fg_color="transparent")
        controls_content.pack(fill="x", padx=20, pady=15)
        controls_content.grid_columnconfigure(0, weight=1)
        
        # Search and filters row
        search_frame = ctk.CTkFrame(controls_content, fg_color="transparent")
        search_frame.grid(row=0, column=0, sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search patients by name, phone, or email...",
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            textvariable=self.search_var
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_var.trace("w", self.on_search_change)
        
        # Gender filter
        gender_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        gender_frame.grid(row=0, column=1, padx=(0, 10))
        
        gender_label = ctk.CTkLabel(
            gender_frame,
            text="Gender:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.app.colors['text_dark']
        )
        gender_label.pack()
        
        self.gender_filter = ctk.CTkComboBox(
            gender_frame,
            values=["All", "Male", "Female", "Other"],
            width=100,
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=11),
            command=self.apply_filters
        )
        self.gender_filter.set("All")
        self.gender_filter.pack()
        
        # Age filter
        age_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        age_frame.grid(row=0, column=2, padx=(0, 10))
        
        age_label = ctk.CTkLabel(
            age_frame,
            text="Age Group:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.app.colors['text_dark']
        )
        age_label.pack()
        
        self.age_filter = ctk.CTkComboBox(
            age_frame,
            values=["All", "0-18", "19-35", "36-55", "56-75", "75+"],
            width=100,
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=11),
            command=self.apply_filters
        )
        self.age_filter.set("All")
        self.age_filter.pack()
        
        # Clear filters button
        clear_btn = ctk.CTkButton(
            search_frame,
            text="🗑️",
            width=40,
            height=40,
            corner_radius=8,
            fg_color=self.app.colors['text_light'],
            hover_color="#5a6268",
            command=self.clear_filters
        )
        clear_btn.grid(row=0, column=3)
    
    def create_data_table(self):
        """Create the main data table with modern styling"""
        # Table container
        table_container = ctk.CTkFrame(
            self,
            corner_radius=10,
            fg_color=self.app.colors['white']
        )
        table_container.grid(row=2, column=0, sticky="nsew", padx=20)
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
        
        # Create treeview with scrollbars
        tree_frame = ctk.CTkFrame(table_container, fg_color="transparent")
        tree_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Configure treeview style
        style = ttk.Style()
        style.theme_use("clam")
        
        # Customize treeview colors
        style.configure("Custom.Treeview",
                       background=self.app.colors['white'],
                       foreground=self.app.colors['text_dark'],
                       fieldbackground=self.app.colors['white'],
                       borderwidth=0,
                       font=('Segoe UI', 10))
        
        style.configure("Custom.Treeview.Heading",
                       background=self.app.colors['primary'],
                       foreground=self.app.colors['white'],
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0)
        
        style.map("Custom.Treeview",
                 background=[("selected", self.app.colors['background'])],
                 foreground=[("selected", self.app.colors['text_dark'])])
        
        # Create treeview
        columns = ("ID", "Name", "Age", "Gender", "Phone", "Email", "Last Visit", "Actions")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
            height=15
        )
        
        # Configure columns
        column_widths = {"ID": 80, "Name": 200, "Age": 80, "Gender": 100, 
                        "Phone": 150, "Email": 200, "Last Visit": 120, "Actions": 150}
        
        for col in columns:
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, width=column_widths.get(col, 100), anchor="w")
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Bind events
        self.tree.bind("<Double-Button-1>", self.on_row_double_click)
        self.tree.bind("<Button-3>", self.show_context_menu)  # Right click\n    \n    def create_pagination(self):\n        \"\"\"Create pagination controls\"\"\"\n        pagination_frame = ctk.CTkFrame(self, fg_color=\"transparent\")\n        pagination_frame.grid(row=3, column=0, sticky=\"ew\", padx=20, pady=(10, 20))\n        pagination_frame.grid_columnconfigure(1, weight=1)\n        \n        # Results info\n        self.results_label = ctk.CTkLabel(\n            pagination_frame,\n            text=\"Showing 1-25 of 1,247 patients\",\n            font=ctk.CTkFont(size=12),\n            text_color=self.app.colors['text_light']\n        )\n        self.results_label.grid(row=0, column=0, sticky=\"w\")\n        \n        # Page controls\n        page_frame = ctk.CTkFrame(pagination_frame, fg_color=\"transparent\")\n        page_frame.grid(row=0, column=2, sticky=\"e\")\n        \n        # Previous button\n        prev_btn = ctk.CTkButton(\n            page_frame,\n            text=\"◀ Previous\",\n            width=80,\n            height=30,\n            font=ctk.CTkFont(size=11),\n            fg_color=self.app.colors['background'],\n            text_color=self.app.colors['text_dark'],\n            hover_color=self.app.colors['text_light'],\n            command=self.previous_page\n        )\n        prev_btn.pack(side=\"left\", padx=(0, 5))\n        \n        # Page info\n        self.page_label = ctk.CTkLabel(\n            page_frame,\n            text=\"Page 1 of 50\",\n            font=ctk.CTkFont(size=12),\n            text_color=self.app.colors['text_dark']\n        )\n        self.page_label.pack(side=\"left\", padx=10)\n        \n        # Next button\n        next_btn = ctk.CTkButton(\n            page_frame,\n            text=\"Next ▶\",\n            width=80,\n            height=30,\n            font=ctk.CTkFont(size=11),\n            fg_color=self.app.colors['background'],\n            text_color=self.app.colors['text_dark'],\n            hover_color=self.app.colors['text_light'],\n            command=self.next_page\n        )\n        next_btn.pack(side=\"left\", padx=(5, 0))\n    \n    def load_sample_data(self):\n        \"\"\"Load sample patient data\"\"\"\n        # Sample data (in real app, this would come from database)\n        self.patients_data = [\n            {\"id\": 1, \"name\": \"John Smith\", \"age\": 45, \"gender\": \"Male\", \n             \"phone\": \"+1-555-0123\", \"email\": \"john.smith@email.com\", \"last_visit\": \"2024-07-10\"},\n            {\"id\": 2, \"name\": \"Sarah Johnson\", \"age\": 32, \"gender\": \"Female\", \n             \"phone\": \"+1-555-0124\", \"email\": \"sarah.j@email.com\", \"last_visit\": \"2024-07-09\"},\n            {\"id\": 3, \"name\": \"Michael Brown\", \"age\": 67, \"gender\": \"Male\", \n             \"phone\": \"+1-555-0125\", \"email\": \"m.brown@email.com\", \"last_visit\": \"2024-07-08\"},\n            {\"id\": 4, \"name\": \"Emily Davis\", \"age\": 28, \"gender\": \"Female\", \n             \"phone\": \"+1-555-0126\", \"email\": \"emily.davis@email.com\", \"last_visit\": \"2024-07-07\"},\n            {\"id\": 5, \"name\": \"Robert Wilson\", \"age\": 55, \"gender\": \"Male\", \n             \"phone\": \"+1-555-0127\", \"email\": \"r.wilson@email.com\", \"last_visit\": \"2024-07-05\"}\n        ]\n        \n        self.filtered_data = self.patients_data.copy()\n        self.populate_table()\n    \n    def populate_table(self):\n        \"\"\"Populate the table with data\"\"\"\n        # Clear existing data\n        for item in self.tree.get_children():\n            self.tree.delete(item)\n        \n        # Add new data\n        for patient in self.filtered_data:\n            values = (\n                patient[\"id\"],\n                patient[\"name\"],\n                patient[\"age\"],\n                patient[\"gender\"],\n                patient[\"phone\"],\n                patient[\"email\"],\n                patient[\"last_visit\"],\n                \"View • Edit • Delete\"\n            )\n            \n            # Add row with alternating colors\n            item = self.tree.insert(\"\", \"end\", values=values)\n            \n            # Add tags for styling (optional)\n            if len(self.tree.get_children()) % 2 == 0:\n                self.tree.set(item, \"#1\", patient[\"id\"])\n    \n    def on_search_change(self, *args):\n        \"\"\"Handle search input changes\"\"\"\n        # Debounce search to avoid too many calls\n        if hasattr(self, '_search_timer'):\n            self.after_cancel(self._search_timer)\n        self._search_timer = self.after(300, self.apply_filters)\n    \n    def apply_filters(self, *args):\n        \"\"\"Apply search and filter criteria\"\"\"\n        search_term = self.search_var.get().lower()\n        gender_filter = self.gender_filter.get()\n        age_filter = self.age_filter.get()\n        \n        # Filter data\n        self.filtered_data = []\n        for patient in self.patients_data:\n            # Search filter\n            if search_term:\n                searchable_text = f\"{patient['name']} {patient['phone']} {patient['email']}\".lower()\n                if search_term not in searchable_text:\n                    continue\n            \n            # Gender filter\n            if gender_filter != \"All\" and patient['gender'] != gender_filter:\n                continue\n            \n            # Age filter\n            if age_filter != \"All\":\n                age = patient['age']\n                if age_filter == \"0-18\" and not (0 <= age <= 18):\n                    continue\n                elif age_filter == \"19-35\" and not (19 <= age <= 35):\n                    continue\n                elif age_filter == \"36-55\" and not (36 <= age <= 55):\n                    continue\n                elif age_filter == \"56-75\" and not (56 <= age <= 75):\n                    continue\n                elif age_filter == \"75+\" and age <= 75:\n                    continue\n            \n            self.filtered_data.append(patient)\n        \n        # Update table\n        self.populate_table()\n        \n        # Update results label\n        total = len(self.filtered_data)\n        self.results_label.configure(text=f\"Showing {min(25, total)} of {total} patients\")\n    \n    def clear_filters(self):\n        \"\"\"Clear all filters and search\"\"\"\n        self.search_var.set(\"\")\n        self.gender_filter.set(\"All\")\n        self.age_filter.set(\"All\")\n        self.apply_filters()\n    \n    def on_row_double_click(self, event):\n        \"\"\"Handle double-click on table row\"\"\"\n        selection = self.tree.selection()\n        if selection:\n            item = self.tree.item(selection[0])\n            patient_id = item['values'][0]\n            self.view_patient_details(patient_id)\n    \n    def show_context_menu(self, event):\n        \"\"\"Show context menu on right-click\"\"\"\n        # Select the row under cursor\n        row_id = self.tree.identify_row(event.y)\n        if row_id:\n            self.tree.selection_set(row_id)\n            \n            # Create context menu\n            context_menu = tk.Menu(self, tearoff=0)\n            context_menu.add_command(label=\"👁️ View Details\", command=lambda: self.view_patient_details())\n            context_menu.add_command(label=\"✏️ Edit Patient\", command=lambda: self.edit_patient())\n            context_menu.add_separator()\n            context_menu.add_command(label=\"📋 New Visit\", command=lambda: self.new_visit_for_patient())\n            context_menu.add_command(label=\"📅 Schedule Appointment\", command=lambda: self.schedule_appointment())\n            context_menu.add_separator()\n            context_menu.add_command(label=\"🗑️ Delete Patient\", command=lambda: self.delete_patient())\n            \n            # Show menu\n            try:\n                context_menu.tk_popup(event.x_root, event.y_root)\n            finally:\n                context_menu.grab_release()\n    \n    def view_patient_details(self, patient_id=None):\n        \"\"\"View patient details\"\"\"\n        if not patient_id:\n            selection = self.tree.selection()\n            if selection:\n                patient_id = self.tree.item(selection[0])['values'][0]\n        \n        if patient_id:\n            messagebox.showinfo(\"Patient Details\", f\"Opening details for patient ID: {patient_id}\")\n            # In real app, this would open a detailed patient view\n    \n    def edit_patient(self):\n        \"\"\"Edit selected patient\"\"\"\n        selection = self.tree.selection()\n        if selection:\n            patient_id = self.tree.item(selection[0])['values'][0]\n            messagebox.showinfo(\"Edit Patient\", f\"Opening edit form for patient ID: {patient_id}\")\n            # In real app, this would open an edit form\n    \n    def new_visit_for_patient(self):\n        \"\"\"Create new visit for selected patient\"\"\"\n        selection = self.tree.selection()\n        if selection:\n            patient_id = self.tree.item(selection[0])['values'][0]\n            messagebox.showinfo(\"New Visit\", f\"Creating new visit for patient ID: {patient_id}\")\n            # In real app, this would open visit form with patient pre-selected\n    \n    def schedule_appointment(self):\n        \"\"\"Schedule appointment for selected patient\"\"\"\n        selection = self.tree.selection()\n        if selection:\n            patient_id = self.tree.item(selection[0])['values'][0]\n            messagebox.showinfo(\"Schedule Appointment\", f\"Scheduling appointment for patient ID: {patient_id}\")\n    \n    def delete_patient(self):\n        \"\"\"Delete selected patient\"\"\"\n        selection = self.tree.selection()\n        if selection:\n            patient_name = self.tree.item(selection[0])['values'][1]\n            if messagebox.askyesno(\"Confirm Delete\", f\"Are you sure you want to delete patient '{patient_name}'?\\n\\nThis action cannot be undone.\"):\n                # In real app, delete from database\n                self.tree.delete(selection[0])\n                messagebox.showinfo(\"Success\", f\"Patient '{patient_name}' has been deleted.\")\n    \n    def export_data(self):\n        \"\"\"Export table data\"\"\"\n        messagebox.showinfo(\"Export\", \"Exporting patient data to CSV file...\")\n        # In real app, this would export the filtered data to CSV/Excel\n    \n    def previous_page(self):\n        \"\"\"Go to previous page\"\"\"\n        print(\"Previous page clicked\")\n    \n    def next_page(self):\n        \"\"\"Go to next page\"\"\"\n        print(\"Next page clicked\")

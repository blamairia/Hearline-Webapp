# HeartLine Medical Clinic - Modern Desktop Application

A beautiful, responsive, and professional desktop version of the HeartLine Medical Clinic web application, built with **CustomTkinter** for a modern, native desktop experience.

## 🎯 Overview

This modern desktop application replicates the complete functionality of the HeartLine Flask web application with:

- **Modern GUI Framework**: Built with CustomTkinter for native desktop experience
- **Medical-Themed Design**: Professional blue gradient theme matching the original web app
- **Responsive Layout**: Collapsible sidebar and adaptive content areas
- **Smooth Animations**: Hover effects, transitions, and modern interactions
- **Professional UI/UX**: Clean, intuitive interface designed for medical professionals

## 🚀 Features

### ✨ Modern UI Components
- **Responsive Sidebar Navigation** with collapse functionality
- **Dashboard with Statistics Cards** showing key metrics
- **Professional Forms** with validation and modern styling
- **Data Tables** with search, filter, and sort capabilities
- **Interactive Charts** for ECG waveform visualization
- **Theme Toggle** (Light/Dark mode support)
- **Status Bar** with real-time updates

### 🏥 Medical Functionality
- **Patient Management** - Create, edit, and view patient records
- **Visit Documentation** - Comprehensive visit forms with ECG integration
- **Appointment Scheduling** - Calendar-based appointment management
- **ECG Analysis** - Real-time ECG waveform analysis and visualization
- **Medical Records** - Secure storage and retrieval of patient data
- **Prescription Management** - Digital prescription creation and tracking

### 🎨 Design Features
- **Medical Color Scheme** - Professional blue gradients (#0074d9, #00b4ff)
- **FontAwesome Icons** - Consistent iconography throughout the app
- **Smooth Animations** - Hover effects and smooth transitions
- **Responsive Layout** - Adapts to different screen sizes
- **Modern Typography** - Clean, readable fonts with proper hierarchy

## 📁 Project Structure

```
modern_ui/
├── src/
│   ├── main.py                 # Main application class
│   ├── components/             # Reusable UI components
│   ├── views/                  # Application views/screens
│   └── utils/                  # Utility functions
├── assets/
│   ├── images/                 # Logo and images
│   └── icons/                  # Application icons
├── requirements.txt            # Python dependencies
├── run_app.py                 # Application launcher
└── README.md                  # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Windows 10/11 (CustomTkinter works best on Windows)

### Quick Start

1. **Navigate to the project directory:**
   ```bash
   cd "d:\projects\Hearline Webapp\desktop-build\modern_ui"
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python run_app.py
   ```

### Core Dependencies
```
customtkinter>=5.2.0    # Modern GUI framework
pillow>=10.0.0          # Image processing
matplotlib>=3.7.0       # Chart plotting
pandas>=2.0.0           # Data handling
```

## 🎮 How to Use

### Navigation
- **Sidebar Menu**: Click any menu item to navigate between sections
- **Quick Actions**: Use the top-right buttons for common tasks
- **Collapsible Sidebar**: Hover and click to expand/collapse
- **Theme Toggle**: Switch between light and dark themes in Settings

### Key Sections

#### 📊 Dashboard
- Overview of clinic statistics
- Recent activity feed
- Quick access to common functions
- Key performance indicators

#### 👤 New Patient
- Modern form with validation
- Organized field layout
- Real-time input feedback
- Save/cancel functionality

#### 📋 New Visit
- Comprehensive visit documentation
- ECG file upload and analysis
- Medical history integration
- Prescription management

#### 👥 Patients Table
- Searchable patient database
- Filter and sort capabilities
- Quick edit and view actions
- Export functionality

#### 📅 Appointments
- Calendar-based scheduling
- Appointment status tracking
- Patient integration
- Reminder system

#### 💓 ECG History
- ECG waveform visualization
- Analysis results display
- Historical trend analysis
- Export and print options

## 🎨 UI/UX Design Principles

### Color Scheme
```python
colors = {
    'primary': '#0074d9',          # Main blue
    'primary_dark': '#0056b3',     # Darker blue  
    'secondary': '#00b4ff',        # Light blue
    'success': '#28a745',          # Green
    'warning': '#ffc107',          # Yellow
    'danger': '#dc3545',           # Red
    'background': '#f8f9fa',       # Light gray
    'white': '#ffffff',
    'text_dark': '#212529',
    'text_light': '#6c757d'
}
```

### Typography
- **Headers**: CTkFont(size=24-32, weight="bold")
- **Subheaders**: CTkFont(size=18-20, weight="bold")
- **Body Text**: CTkFont(size=14, weight="normal")
- **Buttons**: CTkFont(size=12-16, weight="bold")

### Layout Principles
- **Sidebar**: Fixed 250px width, collapsible to 60px
- **Content Area**: Responsive with 20px padding
- **Cards**: 15px border radius, subtle shadows
- **Buttons**: 40-50px height, rounded corners
- **Forms**: Organized in logical groups with clear labels

## 🔧 Customization

### Themes
The application supports both light and dark themes:
```python
ctk.set_appearance_mode("light")  # or "dark" or "system"
ctk.set_default_color_theme("blue")
```

### Colors
Modify the color scheme in `main.py`:
```python
self.colors = {
    'primary': '#your_color',
    # ... other colors
}
```

### Adding New Views
1. Create content method in `main.py`
2. Add navigation item to `nav_items`
3. Implement the view logic
4. Add any required assets

## 🚀 Advanced Features

### Real-time Updates
- Status bar shows current time
- Live database connection status
- Automatic refresh of critical data

### Animations
- Smooth hover effects on buttons
- Fade-in transitions for content
- Scale animations on card hover
- Loading spinners for async operations

### Accessibility
- Keyboard navigation support
- High contrast mode compatibility
- Screen reader friendly labels
- Proper focus management

## 📈 Performance

### Optimizations
- **Lazy Loading**: Views loaded only when needed
- **Memory Management**: Proper widget cleanup
- **Efficient Rendering**: CustomTkinter's optimized drawing
- **Responsive UI**: Non-blocking operations

### System Requirements
- **RAM**: 4GB minimum, 8GB recommended
- **CPU**: Dual-core processor minimum
- **Storage**: 100MB for application
- **Display**: 1280x720 minimum resolution

## 🔒 Security Features

### Data Protection
- No hardcoded credentials
- Environment variable configuration
- Secure database connections
- Input validation and sanitization

### User Management
- Role-based access control
- Session management
- Audit logging
- Password encryption

## 🛠️ Development

### Adding New Features
1. Plan the UI layout
2. Create the view method
3. Add navigation entry
4. Implement business logic
5. Test thoroughly

### Debugging
- Enable debug mode in CustomTkinter
- Use print statements for flow tracing
- Check console for error messages
- Test on different screen sizes

## 📦 Building for Distribution

### Creating Executable
```bash
pip install pyinstaller
pyinstaller --onefile --windowed run_app.py
```

### Distribution Package
1. Bundle all dependencies
2. Include assets and icons
3. Create installer (optional)
4. Test on clean systems

## 🤝 Contributing

### Development Guidelines
- Follow PEP 8 style guidelines
- Use type hints where applicable
- Add docstrings to all methods
- Test on multiple screen resolutions

### Reporting Issues
- Use descriptive titles
- Include steps to reproduce
- Attach screenshots if applicable
- Specify system information

## 📄 License

This project is part of the HeartLine Medical Clinic system and follows the same licensing terms as the main application.

## 🙏 Acknowledgments

- **CustomTkinter**: For the modern GUI framework
- **Pillow**: For image processing capabilities
- **Matplotlib**: For chart and graph generation
- **Original Flask App**: For design inspiration and functionality reference

---

**Built with ❤️ for medical professionals**

🏥 **HeartLine Medical Clinic Desktop Application**  
*Modern • Responsive • Professional*

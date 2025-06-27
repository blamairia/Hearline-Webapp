# 🏥 Heartline Desktop - AI-Powered Doct### **🐍 Recommended: Conda Environment Setup**

```bash
# Option 1: Using environment.yml (Easiest)
conda env create -f environment.yml
conda activate heartline-desktop

# Option 2: Manual setup
conda create -n heartline-desktop python=3.10
conda activate heartline-desktop
pip install -r requirements-pyside.txt

# Run setup and launch
python setup.py
python main.py
```ement System

## 🚀 Overview

**Heartline Desktop** is a cutting-edge doctor cabinet management system built with **PyQt6** and **Material Design**. It provides the same powerful core functionalities as the web application with a native desktop experience, featuring **AI-powered ECG analysis** and comprehensive patient management.

### 🎯 **Why Desktop?**
- **Native Performance**: Faster UI responsiveness and better resource management
- **Offline Capabilities**: Work without internet connectivity
- **Enhanced Security**: Local data processing and storage
- **Professional Interface**: Modern Material Design with medical workflow optimization
- **Advanced Features**: Desktop-specific functionalities like system notifications and file associations

## ✨ Features

- **Patient Management**: Complete CRUD operations for patient records
- **Doctor Management**: Multi-doctor support with role-based access
- **Appointment Scheduling**: Advanced scheduling with calendar view
- **ECG Analysis**: AI-powered ECG analysis using ONNX Runtime
- **Visit Management**: Comprehensive visit documentation
- **Prescription Management**: Integration with 7000+ Algerian medications
- **Waiting List**: Real-time patient queue management
- **Clinic Management**: Multi-clinic support and settings

## 🛠️ Technology Stack

- **Framework**: PyQt6 with Material Design
- **Database**: PostgreSQL (same as web app)
- **AI Engine**: ONNX Runtime for ECG analysis
- **Architecture**: Clean Architecture with Repository Pattern
- **UI Components**: Material Design with modern themes

## 🚀 Quick Start

### **Prerequisites**
- **Python 3.9-3.11** (recommended: **Python 3.10**)
- PostgreSQL database (or SQLite for testing)
- Git
- Conda (recommended for Windows) or pip

### **� Recommended: Conda Environment Setup**

```bash
# Create conda environment with Python 3.10
conda create -n heartline-desktop python=3.10

# Activate environment
conda activate heartline-desktop

# Install dependencies
pip install -r requirements-pyside.txt

# Run setup and launch
python setup.py
python main.py
```

### **🔧 Alternative: Quick pip Installation (Windows)**

```bash
# 1. Install GUI framework (choose one)
pip install PySide6==6.4.2                    # Recommended for Windows
# OR
pip install -r requirements-pyside.txt        # All dependencies

# 2. Test installation
python main_simple.py                         # Demo window

# 3. Configure database (.env file)
copy .env.example .env
# Edit .env with your database credentials

# 4. Run setup
python setup.py

# 5. Launch application
python main.py
```

### **⚡ Troubleshooting**

If you encounter installation issues:

1. **PyQt6 fails**: Use PySide6 instead (more stable on Windows)
2. **Missing modules**: Try `python main_simple.py` for basic test
3. **Database errors**: Check .env configuration
4. **ONNX model missing**: Copy from parent directory

📖 **See [INSTALLATION.md](INSTALLATION.md) for detailed troubleshooting guide**

## 📁 Project Structure

```
heartline-desktop/
├── main.py                 # Application entry point
├── main_simple.py          # Simple launcher with Qt detection
├── setup.py               # Automated setup script
├── quick_check.py          # Python version and environment checker
├── environment.yml         # Conda environment specification
├── requirements.txt        # PyQt6 dependencies
├── requirements-pyside.txt # PySide6 dependencies (Windows-friendly)
├── .env.example           # Environment variables template
├── README.md              # This file
├── INSTALLATION.md        # Detailed installation guide
├── DEVELOPMENT.md         # Development documentation
├── src/
│   ├── __init__.py
│   ├── core/              # Core business logic
│   │   ├── __init__.py
│   │   ├── config.py      # Configuration management
│   │   ├── database.py    # Database connection and management
│   │   └── exceptions.py  # Custom exceptions
│   ├── models/            # Database models
│   │   ├── __init__.py
│   │   ├── base.py        # Base model class
│   │   ├── patient.py     # Patient model
│   │   ├── doctor.py      # Doctor model
│   │   ├── appointment.py # Appointment model
│   │   ├── visit.py       # Visit model
│   │   └── ...           # Other models
│   ├── repositories/      # Data access layer
│   │   ├── __init__.py
│   │   ├── base.py        # Base repository
│   │   ├── patient.py     # Patient repository
│   │   └── ...           # Other repositories
│   ├── services/          # Business logic layer
│   │   ├── __init__.py
│   │   ├── patient.py     # Patient service
│   │   ├── ecg_analysis.py # ECG analysis service
│   │   └── ...           # Other services
│   ├── ui/               # User interface
│   │   ├── __init__.py
│   │   ├── main_window.py # Main application window
│   │   ├── components/    # Reusable UI components
│   │   ├── dialogs/       # Dialog windows
│   │   ├── widgets/       # Custom widgets
│   │   └── resources/     # UI resources
│   └── utils/            # Utility functions
│       ├── __init__.py
│       ├── validators.py  # Data validation
│       └── helpers.py     # Helper functions
├── assets/               # Static assets
│   ├── icons/            # Application icons
│   ├── images/           # Images and graphics
│   └── themes/           # UI themes
├── models/               # AI models
│   └── resnet34_ecg.onnx # ECG analysis model
└── logs/                 # Application logs
```

## 🔧 Configuration

The application uses environment variables for configuration:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=heartline

# Application Settings
APP_NAME=Heartline Desktop
APP_VERSION=1.0.0
DEBUG=false

# AI Model
ONNX_MODEL_PATH=models/resnet34_ecg.onnx

# UI Theme
THEME=dark_blue.xml
```

## 🎨 UI Components

The application uses Material Design components for a modern, consistent user interface:

- **Material Cards**: For displaying patient information
- **Material Buttons**: For actions and navigation
- **Material Tables**: For data display
- **Material Forms**: For data input
- **Material Dialogs**: For confirmations and forms
- **Dark/Light Themes**: User preference support

## 🏗️ Architecture

The application follows Clean Architecture principles:

1. **Presentation Layer** (UI): PyQt6 widgets and windows
2. **Application Layer** (Services): Business logic and use cases
3. **Domain Layer** (Models): Core business entities
4. **Infrastructure Layer** (Repositories): Data access and external services

## 📊 Key Features

### Patient Management
- Advanced search and filtering
- Complete medical history
- Insurance information
- Emergency contacts

### ECG Analysis
- Real-time AI-powered analysis
- 9-class cardiac condition detection
- Confidence scoring
- Historical analysis comparison

### Appointment System
- Calendar view with drag-and-drop
- Recurring appointments
- Automated reminders
- Conflict detection

### Prescription Management
- 7000+ Algerian medication database
- Drug interaction warnings
- Dosage recommendations
- Prescription printing

## 🚀 Performance

- **Fast Startup**: Optimized initialization
- **Responsive UI**: Asynchronous operations
- **Memory Efficient**: Smart caching strategies
- **Database Optimization**: Connection pooling

## 🔒 Security

- **User Authentication**: Role-based access control
- **Data Encryption**: Sensitive data protection
- **Audit Logging**: Complete action tracking
- **Backup Integration**: Automated data backup

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Heartline Desktop** - Revolutionizing healthcare management with modern technology.

# 🛠️ Heartline Desktop Installation Guide

## � **Recommended: Conda Environment Setup**

### **Prerequisites**
- **Python 3.9-3.11** (recommended: **Python 3.10**)
- Anaconda or Miniconda installed
- PostgreSQL (optional for production)

### **Step 1: Create Conda Environment**

**Option A: Using environment.yml (Recommended)**
```bash
# Create environment from file
conda env create -f environment.yml

# Activate the environment
conda activate heartline-desktop
```

**Option B: Manual creation**
```bash
# Create new environment with Python 3.10
conda create -n heartline-desktop python=3.10

# Activate the environment
conda activate heartline-desktop

# Verify Python version
python --version
```

### **Step 2: Install Dependencies**

```bash
# Install all requirements (PySide6 recommended for Windows)
pip install -r requirements-pyside.txt

# Alternative: Manual installation
pip install PySide6==6.4.2 qt-material==2.14 psycopg2-binary==2.9.9
```

### **Step 3: Setup and Launch**

```bash
# Run setup script
python setup.py

# Launch application
python main.py
```

---

## �🚨 **Alternative: Quick Fix for Installation Issues**

If you're experiencing installation problems, follow this step-by-step guide:

### **Step 1: Install PySide6 (Recommended for Windows)**

```bash
# Option 1: Install PySide6 (more stable on Windows)
pip install PySide6==6.4.2

# Option 2: Install all dependencies with PySide6
pip install -r requirements-pyside.txt
```

### **Step 2: Test Basic Installation**

```bash
# Test if Qt framework is working
python main_simple.py
```

This will open a demo window to verify the Qt framework is working correctly.

### **Step 3: Configure Database**

```bash
# Copy environment template
copy .env.example .env

# Edit .env file with your database credentials:
# DB_HOST=localhost
# DB_PORT=5432
# DB_USER=postgres
# DB_PASSWORD=your_password
# DB_NAME=heartline
```

### **Step 4: Run Setup Script**

```bash
# Run the setup script to create directories and check dependencies
python setup.py
```

### **Step 5: Copy ONNX Model**

```bash
# Copy the ECG analysis model from the parent directory
copy "..\resnet34_model.onnx" "models\resnet34_ecg.onnx"
```

### **Step 6: Launch Full Application**

```bash
# Try launching the full application
python main.py

# If that fails, use the simple launcher
python main_simple.py
```

## 🔧 **Troubleshooting Common Issues**

### **Issue 1: PyQt6 Installation Fails**
```bash
# Solution: Use PySide6 instead
pip uninstall PyQt6 PyQt6-Qt6
pip install PySide6==6.4.2
```

### **Issue 2: "ModuleNotFoundError: No module named 'PyQt6'"**
```bash
# Solution: Install PySide6 or fix PyQt6
pip install PySide6==6.4.2
python main_simple.py  # Test with simple launcher
```

### **Issue 3: Database Connection Errors**
```bash
# Check .env file exists and has correct values
# Ensure PostgreSQL is running
# Test connection from web app first
```

### **Issue 4: ONNX Model Not Found**
```bash
# Copy model from parent directory
copy "..\resnet34_model.onnx" "models\resnet34_ecg.onnx"

# Or download from repository if needed
# Check models/ directory exists
```

## 📦 **Alternative Installation Methods**

### **Method 1: Minimal Installation (GUI Only)**
```bash
# Install only GUI components for testing
pip install PySide6==6.4.2 python-dotenv
python main_simple.py
```

### **Method 2: Full Installation (All Features)**
```bash
# Install all dependencies for complete functionality
pip install -r requirements-pyside.txt
python setup.py
python main.py
```

### **Method 3: Conda Environment (Recommended)**
```bash
# Create new conda environment
conda create -n heartline-desktop python=3.10
conda activate heartline-desktop
pip install -r requirements-pyside.txt
```

## 🖥️ **Platform-Specific Notes**

### **Windows**
- Use `requirements-pyside.txt` for better compatibility
- Use PowerShell or Command Prompt
- Ensure Visual C++ Redistributable is installed

### **macOS**
- Both PyQt6 and PySide6 should work
- May need Xcode command line tools

### **Linux**
- Install system dependencies: `sudo apt-get install python3-dev`
- Both PyQt6 and PySide6 should work

## ✅ **Verification Steps**

1. **Test Qt Framework**: `python main_simple.py`
2. **Check Dependencies**: `python setup.py`
3. **Verify Database**: Check .env configuration
4. **Test ONNX Model**: Ensure model file exists
5. **Launch Application**: `python main.py`

## 🆘 **Getting Help**

If you're still having issues:

1. **Check Python Version**: Ensure Python 3.8+
2. **Update pip**: `pip install --upgrade pip`
3. **Clear Cache**: `pip cache purge`
4. **Try Virtual Environment**: Create fresh environment
5. **Check System Requirements**: Ensure all system dependencies

## 📞 **Support**

For additional support:
- Check DEVELOPMENT.md for technical details
- Review error logs in logs/ directory
- Test with simple demo first
- Ensure web app is working correctly

---

**Remember**: The desktop app uses the same database as the web application, so ensure your web app is properly configured first!

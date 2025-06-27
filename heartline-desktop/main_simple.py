"""
Heartline Desktop Application - Simplified Launcher

This version automatically detects available Qt framework (PyQt6 or PySide6)
and provides fallback options for easier setup.
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def check_qt_framework():
    """Check which Qt framework is available"""
    try:
        import PyQt6
        return "PyQt6"
    except ImportError:
        pass
    
    try:
        import PySide6
        return "PySide6"
    except ImportError:
        pass
    
    return None

def main():
    """Main entry point with Qt framework detection"""
    
    print("🏥 Heartline Desktop Application")
    print("=" * 40)
    
    # Check Qt framework availability
    qt_framework = check_qt_framework()
    
    if qt_framework is None:
        print("❌ No Qt framework found!")
        print("\n📦 Please install one of the following:")
        print("Option 1 (Recommended for Windows):")
        print("  pip install -r requirements-pyside.txt")
        print("\nOption 2 (Alternative):")
        print("  pip install PySide6==6.4.2")
        print("\nOption 3 (If you prefer PyQt6):")
        print("  pip install PyQt6==6.4.2")
        sys.exit(1)
    
    print(f"✅ Using {qt_framework}")
    
    # Check other dependencies
    missing_deps = []
    required_packages = ['sqlalchemy', 'psycopg2', 'numpy', 'onnxruntime']
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_deps.append(package)
    
    if missing_deps:
        print(f"❌ Missing dependencies: {', '.join(missing_deps)}")
        print("Please install requirements:")
        if qt_framework == "PySide6":
            print("  pip install -r requirements-pyside.txt")
        else:
            print("  pip install -r requirements.txt")
        sys.exit(1)
    
    # Check database configuration
    from dotenv import load_dotenv
    load_dotenv()
    
    db_vars = ['DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
    missing_db_vars = [var for var in db_vars if not os.getenv(var)]
    
    if missing_db_vars:
        print(f"⚠️  Missing database configuration: {', '.join(missing_db_vars)}")
        print("Please check your .env file")
    
    # Try to import and run the application
    try:
        # Import the main application
        from main import main as run_app
        
        print("🚀 Starting application...")
        run_app()
        
    except ImportError as e:
        print(f"❌ Failed to import application modules: {e}")
        print("Running simplified demo instead...")
        run_simple_demo(qt_framework)
    except Exception as e:
        print(f"❌ Application error: {e}")
        print("Running simplified demo instead...")
        run_simple_demo(qt_framework)

def run_simple_demo(qt_framework):
    """Run a simple demo if full application fails"""
    
    if qt_framework == "PyQt6":
        from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
        from PyQt6.QtCore import Qt
    else:  # PySide6
        from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
        from PySide6.QtCore import Qt
    
    app = QApplication(sys.argv)
    
    # Create simple window
    window = QMainWindow()
    window.setWindowTitle("Heartline Desktop - Demo")
    window.setGeometry(100, 100, 800, 600)
    
    # Central widget
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    # Layout
    layout = QVBoxLayout(central_widget)
    
    # Content
    title = QLabel("🏥 Heartline Desktop")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
    layout.addWidget(title)
    
    subtitle = QLabel("Demo Version - Basic UI Test")
    subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
    subtitle.setStyleSheet("font-size: 16px; color: #666; margin-bottom: 20px;")
    layout.addWidget(subtitle)
    
    info = QLabel(f"Qt Framework: {qt_framework}\nPython: {sys.version_info.major}.{sys.version_info.minor}")
    info.setAlignment(Qt.AlignmentFlag.AlignCenter)
    info.setStyleSheet("font-size: 12px; color: #888;")
    layout.addWidget(info)
    
    status = QLabel("✅ Desktop application framework is working!")
    status.setAlignment(Qt.AlignmentFlag.AlignCenter)
    status.setStyleSheet("font-size: 14px; color: green; margin: 20px;")
    layout.addWidget(status)
    
    next_steps = QLabel(
        "Next steps:\n"
        "1. Configure database in .env file\n"
        "2. Install missing dependencies\n"
        "3. Copy ONNX model to models/ directory\n"
        "4. Run full application"
    )
    next_steps.setAlignment(Qt.AlignmentFlag.AlignCenter)
    next_steps.setStyleSheet("font-size: 12px; margin: 20px;")
    layout.addWidget(next_steps)
    
    window.show()
    
    print("✅ Demo window opened successfully!")
    print("Close the window to exit.")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

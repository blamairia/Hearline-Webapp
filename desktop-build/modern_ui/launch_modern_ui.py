"""
HeartLine Modern Desktop UI Launcher
Installs dependencies and launches the modern desktop application
"""

import subprocess
import sys
import os
from pathlib import Path
import pkg_resources

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3.8, 0):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ Error: requirements.txt not found")
        return False
    
    try:
        # Install requirements
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'customtkinter',
        'pillow',
        'matplotlib',
        'pandas',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            pkg_resources.get_distribution(package)
            print(f"✅ {package} is installed")
        except pkg_resources.DistributionNotFound:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    return len(missing_packages) == 0, missing_packages

def launch_application():
    """Launch the HeartLine desktop application"""
    print("🚀 Launching HeartLine Modern Desktop UI...")
    
    # Add the src directory to Python path
    src_path = Path(__file__).parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    
    try:
        # Import and run the main application
        from main import HeartLineDesktopApp
        
        app = HeartLineDesktopApp()
        app.run()
        
    except ImportError as e:
        print(f"❌ Error importing application: {e}")
        print("   Make sure all dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        return False
    
    return True

def main():
    """Main launcher function"""
    print("=" * 60)
    print("🏥 HeartLine Medical Clinic - Modern Desktop UI")
    print("   Beautiful, Responsive, Professional Interface")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    # Check dependencies
    deps_ok, missing = check_dependencies()
    
    if not deps_ok:
        print(f"📦 Missing packages: {', '.join(missing)}")
        install_choice = input("Would you like to install missing packages? (y/n): ").lower()
        
        if install_choice in ['y', 'yes']:
            if not install_requirements():
                input("Press Enter to exit...")
                return
        else:
            print("❌ Cannot launch without required packages")
            input("Press Enter to exit...")
            return
    
    # Launch application
    if not launch_application():
        input("Press Enter to exit...")
        return

if __name__ == "__main__":
    main()

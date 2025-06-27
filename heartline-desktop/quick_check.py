#!/usr/bin/env python3
"""
Quick Setup Script for Heartline Desktop Application

This script checks your Python version and provides setup guidance
"""

import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python version detected: {version.major}.{version.minor}.{version.micro}")
    
    if version.major != 3:
        print("❌ Error: Python 3.x is required")
        return False
    
    if version.minor < 9:
        print("⚠️  Warning: Python 3.9+ is recommended")
        print("   Your version may work but is not officially supported")
        return True
    elif version.minor > 11:
        print("⚠️  Warning: Python 3.11+ is newer than tested")
        print("   Most features should work but some dependencies might have issues")
        return True
    else:
        print("✅ Python version is compatible")
        return True

def check_conda():
    """Check if conda is available"""
    try:
        result = subprocess.run(['conda', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Conda detected: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Conda not found")
        return False

def main():
    print("🏥 Heartline Desktop - Quick Setup Check")
    print("=" * 50)
    
    # Check Python version
    python_ok = check_python_version()
    
    # Check operating system
    print(f"💻 Operating System: {platform.system()} {platform.release()}")
    
    # Check conda availability
    conda_available = check_conda()
    
    print("\n📋 Recommendations:")
    print("=" * 30)
    
    if not python_ok:
        print("1. ❌ Install Python 3.9-3.11 first")
        print("   Download from: https://www.python.org/downloads/")
        return
    
    if conda_available:
        print("🎉 Recommended setup (using Conda):")
        print("   conda env create -f environment.yml")
        print("   conda activate heartline-desktop")
        print("   python setup.py")
        print("   python main.py")
    else:
        print("📦 Alternative setup (using pip):")
        if platform.system() == "Windows":
            print("   pip install -r requirements-pyside.txt")
        else:
            print("   pip install -r requirements.txt")
        print("   python setup.py")
        print("   python main.py")
    
    print("\n🔧 Troubleshooting:")
    print("   - For issues, try: python main_simple.py")
    print("   - See INSTALLATION.md for detailed guide")
    print("   - Check .env configuration for database")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
HeartLine Desktop Application Launcher
Main entry point for the modern desktop version of HeartLine Medical Clinic
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Import and run the application
from main import HeartLineDesktopApp

if __name__ == "__main__":
    print("🏥 HeartLine Medical Clinic - Desktop Application")
    print("=" * 50)
    print("🚀 Initializing modern desktop interface...")
    
    try:
        # Create and run the application
        app = HeartLineDesktopApp()
        print("✅ Application initialized successfully!")
        print("🎨 UI Framework: CustomTkinter (Modern)")
        print("💫 Features: Responsive, Animated, Professional")
        print("📱 Design: Medical-themed with blue gradients")
        print("\n🏃 Starting application...")
        
        app.run()
        
    except KeyboardInterrupt:
        print("\n👋 Application closed by user")
        sys.exit(0)
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("\n📦 Please install required packages:")
        print("    pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Application error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

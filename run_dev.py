#!/usr/bin/env python3
"""
Development server runner with auto-reload enabled.
Run this script instead of app.py for development.

Usage: python run_dev.py
"""

import subprocess
import sys
import os

if __name__ == '__main__':
    # Set environment variables for development
    env = os.environ.copy()
    env['FLASK_ENV'] = 'development'
    env['FLASK_DEBUG'] = '1'
    
    print("🚀 Starting HeartLine in Development Mode")
    print("📁 Auto-reload enabled - HTML/CSS changes will refresh automatically")
    print("🔧 Debug mode enabled - detailed error messages available")
    print("🌐 Server will be available at: http://127.0.0.1:5000")
    print("⏹️  Press CTRL+C to stop the server")
    print("-" * 60)
    
    try:
        # Run the Flask app with development settings
        subprocess.run([sys.executable, 'app.py'], env=env, cwd=os.path.dirname(os.path.abspath(__file__)))
    except KeyboardInterrupt:
        print("\n✅ Development server stopped.")
    except Exception as e:
        print(f"❌ Error starting development server: {e}")

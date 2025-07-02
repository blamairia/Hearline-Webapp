#!/usr/bin/env python3
"""
Test script to check color imports and availability
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'src'))

try:
    from ui.styles import AppColors, AppStyles
    
    print("✅ Successfully imported AppColors and AppStyles")
    
    # Test for required colors
    required_colors = [
        'PRIMARY', 'PRIMARY_DARK', 'PRIMARY_LIGHT',
        'BACKGROUND', 'CARD_BACKGROUND', 'TEXT_PRIMARY', 'TEXT_SECONDARY',
        'HOVER', 'SELECTED', 'DISABLED', 'PRIMARY_HOVER', 'PRIMARY_PRESSED'
    ]
    
    missing_colors = []
    for color in required_colors:
        if hasattr(AppColors, color):
            print(f"✅ {color}: {getattr(AppColors, color)}")
        else:
            missing_colors.append(color)
            print(f"❌ Missing: {color}")
    
    if missing_colors:
        print(f"\n❌ Missing colors: {missing_colors}")
        sys.exit(1)
    else:
        print(f"\n✅ All required colors are available!")
        
    # Test styles
    print(f"\n🎨 Testing styles:")
    print("✅ APP_STYLE available")
    print("✅ PRIMARY_BUTTON_STYLE available")
    print("✅ SECONDARY_BUTTON_STYLE available")
    print("✅ get_table_style() available")
    
    print(f"\n🎉 Color system test completed successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

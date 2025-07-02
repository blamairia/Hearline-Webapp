#!/usr/bin/env python3
"""
Database Migration Script - Add Default Doctor Setting

This script adds the default_doctor_id column to the general_settings table.
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.database import db_manager
from sqlalchemy import text

def add_default_doctor_column():
    """Add default_doctor_id column to general_settings table"""
    try:
        print("🚀 Adding default_doctor_id column to general_settings table...")
        
        with db_manager.get_session() as session:
            # Check if column already exists
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='general_settings' AND column_name='default_doctor_id'
            """)
            
            result = session.execute(check_query).fetchone()
            if result:
                print("✅ Column default_doctor_id already exists!")
                return
            
            # Add the column
            add_column_query = text("""
                ALTER TABLE general_settings 
                ADD COLUMN default_doctor_id INTEGER REFERENCES doctor(id)
            """)
            
            session.execute(add_column_query)
            session.commit()
            
            print("✅ Successfully added default_doctor_id column!")
            
    except Exception as e:
        print(f"❌ Error adding column: {str(e)}")
        raise

if __name__ == "__main__":
    # Initialize database first
    db_manager.initialize()
    add_default_doctor_column()
    print("🎉 Migration completed!")

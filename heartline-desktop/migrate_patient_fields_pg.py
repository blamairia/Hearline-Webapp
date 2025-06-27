#!/usr/bin/env python3
"""
PostgreSQL Migration Script for Patient Fields
Adds missing fields to the patient table
"""

import psycopg2
from psycopg2 import sql
import sys
import os

# Add the project root to the path so we can import config
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.config import config

def migrate_patient_table():
    """Add missing fields to patient table"""
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )
        cursor = conn.cursor()
        
        print(f"✅ Connected to database: {config.DB_NAME}")
        
        # List of new columns to add
        new_columns = [
            ("city", "VARCHAR(100)"),
            ("state", "VARCHAR(50)"),
            ("zip_code", "VARCHAR(20)"),
            ("country", "VARCHAR(100)"),
            ("chronic_conditions", "TEXT"),
            ("family_history", "TEXT"),
            ("height", "INTEGER"),
            ("weight", "INTEGER"),
            ("blood_type", "VARCHAR(10)"),
            ("ssn", "VARCHAR(20)"),
            ("id_number", "VARCHAR(50)"),
            ("insurance_group", "VARCHAR(100)"),
            ("preferred_language", "VARCHAR(50)"),
            ("notes", "TEXT")
        ]
        
        # Check which columns already exist
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'patient' AND table_schema = 'public'
        """)
        existing_columns = [row[0] for row in cursor.fetchall()]
        
        print(f"Existing columns: {existing_columns}")
        
        # Add missing columns
        for column_name, column_type in new_columns:
            if column_name not in existing_columns:
                try:
                    alter_sql = sql.SQL("ALTER TABLE patient ADD COLUMN {} {}").format(
                        sql.Identifier(column_name),
                        sql.SQL(column_type)
                    )
                    cursor.execute(alter_sql)
                    print(f"✅ Added column: {column_name} {column_type}")
                except psycopg2.Error as e:
                    print(f"❌ Failed to add column {column_name}: {e}")
            else:
                print(f"⏭️  Column {column_name} already exists")
        
        conn.commit()
        print("\n🎉 Migration completed successfully!")
        
        # Verify the changes
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'patient' AND table_schema = 'public'
            ORDER BY ordinal_position
        """)
        final_columns = cursor.fetchall()
        print(f"\nFinal columns ({len(final_columns)}):")
        for col_name, col_type in final_columns:
            print(f"  - {col_name}: {col_type}")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Starting PostgreSQL patient table migration...")
    print(f"Database: {config.database_url}")
    migrate_patient_table()

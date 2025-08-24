import sqlite3
from datetime import datetime, timedelta
import random

# Connect to database (creates file if doesn't exist)
conn = sqlite3.connect('hospital.db')
cursor = conn.cursor()

# Create tables
def create_tables():
    # Patients table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
    ''')
    
    # Visits table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS visits (
        id INTEGER PRIMARY KEY,
        patient_id INTEGER,
        department TEXT NOT NULL,
        visit_date DATE NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES patients (id)
    )
    ''')
    
    # Symptoms table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS symptoms (
        id INTEGER PRIMARY KEY,
        visit_id INTEGER,
        symptom TEXT NOT NULL,
        FOREIGN KEY (visit_id) REFERENCES visits (id)
    )
    ''')
    
    print("✅ Tables created successfully!")

if __name__ == "__main__":
    create_tables()
    conn.commit()
    conn.close()
    print("Database setup complete!")
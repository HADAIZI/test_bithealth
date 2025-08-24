import sqlite3
from datetime import datetime, timedelta
import random

# Connect to database
conn = sqlite3.connect('hospital.db')
cursor = conn.cursor()

# Extended sample data for 500+ records
first_names = [
    "Andi", "Sari", "Budi", "Maya", "Rudi", "Indira", "Agus", "Lina", "Bambang", "Dian",
    "Hendra", "Rina", "Yanto", "Wulan", "Doni", "Siska", "Eko", "Mira", "Joko", "Tari",
    "Herman", "Fitri", "Wahyu", "Putri", "Bayu", "Nina", "Fajar", "Dewi", "Riski", "Sari",
    "Ahmad", "Ani", "Darma", "Eni", "Fandi", "Gita", "Hadi", "Ika", "Jeni", "Kiki",
    "Luki", "Mega", "Nanda", "Oni", "Peni", "Qori", "Ravi", "Siti", "Tono", "Uni"
]

last_names = [
    "Wijaya", "Dewi", "Santoso", "Lestari", "Hartono", "Sari", "Prasetyo", "Kartika", 
    "Sutrisno", "Purnama", "Kusuma", "Marlina", "Setiawan", "Ramadan", "Wijayanti",
    "Handayani", "Gunawan", "Rahayu", "Nugroho", "Maharani", "Rostina", "Setiadi", 
    "Anggraeni", "Pratama", "Melati", "Kurniawan", "Budiman", "Permana", "Hidayat", "Utami"
]

departments = ["Neurology", "Cardiology", "Orthopedics", "Gastroenterology", "General Medicine", "Dermatology"]

# Symptoms by department for realism
symptoms_by_dept = {
    "Neurology": ["pusing", "sakit kepala", "kehilangan keseimbangan", "sulit berjalan", "kesemutan", "lemah otot", "kejang", "mual", "vertigo", "migrain"],
    "Cardiology": ["sesak napas", "nyeri dada", "jantung berdebar", "bengkak kaki", "mudah lelah", "pusing", "nyeri lengan", "keringat dingin"],
    "Orthopedics": ["nyeri sendi", "bengkak", "sulit bergerak", "kaku otot", "memar", "nyeri punggung", "nyeri lutut", "patah tulang"],
    "Gastroenterology": ["mual", "sakit perut", "diare", "muntah", "kembung", "heartburn", "kehilangan nafsu makan", "sembelit"],
    "General Medicine": ["demam", "batuk", "pilek", "sakit tenggorokan", "lemah", "pusing", "mual", "flu"],
    "Dermatology": ["gatal", "ruam", "kulit kering", "bengkak", "kemerahan", "nyeri kulit", "jerawat", "eksim"]
}

def generate_random_date(days_ago=365):
    """Generate random date within last year"""
    base_date = datetime.now()
    random_days = random.randint(1, days_ago)
    return (base_date - timedelta(days=random_days)).strftime('%Y-%m-%d')

def clear_database():
    """Clear all existing data"""
    cursor.execute("DELETE FROM symptoms")
    cursor.execute("DELETE FROM visits") 
    cursor.execute("DELETE FROM patients")
    conn.commit()
    print("Database cleared")

def insert_patients(num_patients=500):
    """Insert patients with varied ages"""
    patients_data = []
    
    for i in range(num_patients):
        # Generate random name
        first = random.choice(first_names)
        last = random.choice(last_names)
        name = f"{first} {last}"
        
        # Ensure good distribution of ages >50 for our query
        if i % 3 == 0:  # Every 3rd patient is >50 (about 167 patients)
            age = random.randint(51, 85)
        else:
            age = random.randint(18, 75)
        
        patients_data.append((name, age))
    
    cursor.executemany("INSERT INTO patients (name, age) VALUES (?, ?)", patients_data)
    print(f"Inserted {len(patients_data)} patients")

def insert_visits_and_symptoms():
    """Insert visits and symptoms with proper relationships"""
    # Get all patients
    cursor.execute("SELECT id, name, age FROM patients")
    patients = cursor.fetchall()
    
    total_visits = 0
    total_symptoms = 0
    
    for patient_id, name, age in patients:
        # Each patient gets 1-4 visits
        num_visits = random.randint(1, 4)
        
        for _ in range(num_visits):
            department = random.choice(departments)
            visit_date = generate_random_date()
            
            # Insert visit
            cursor.execute(
                "INSERT INTO visits (patient_id, department, visit_date) VALUES (?, ?, ?)",
                (patient_id, department, visit_date)
            )
            visit_id = cursor.lastrowid
            total_visits += 1
            
            # Generate symptoms for this visit
            available_symptoms = symptoms_by_dept[department]
            
            # Ensure plenty of Neurology visits with ≥3 symptoms for patients >50
            if age > 50 and department == "Neurology":
                # 80% chance of having ≥3 symptoms
                if random.random() > 0.2:
                    num_symptoms = random.randint(3, 6)
                else:
                    num_symptoms = random.randint(1, 3)
            else:
                num_symptoms = random.randint(1, 5)
            
            # Select random symptoms (no duplicates)
            selected_symptoms = random.sample(available_symptoms, 
                                           min(num_symptoms, len(available_symptoms)))
            
            # Insert symptoms
            for symptom in selected_symptoms:
                cursor.execute(
                    "INSERT INTO symptoms (visit_id, symptom) VALUES (?, ?)",
                    (visit_id, symptom)
                )
                total_symptoms += 1
    
    print(f"Inserted {total_visits} visits and {total_symptoms} symptoms")

def verify_query_data():
    """Verify we have enough data for the query"""
    cursor.execute("""
    SELECT COUNT(*) as total_matches
    FROM patients p
    JOIN visits v ON p.id = v.patient_id  
    JOIN symptoms s ON v.id = s.visit_id
    WHERE p.age > 50 AND v.department = 'Neurology'
    GROUP BY p.id, v.id
    HAVING COUNT(s.symptom) >= 3
    """)
    
    results = cursor.fetchall()
    total_matching_visits = len(results)
    
    print(f"Query-ready visits: {total_matching_visits}")

if __name__ == "__main__":
    print("Inserting data...")
    
    clear_database()
    insert_patients(500)
    insert_visits_and_symptoms()
    
    conn.commit()
    verify_query_data()
    
    print("Data insertion complete")
    conn.close()
import sqlite3

# Connect to database
conn = sqlite3.connect('hospital.db')
cursor = conn.cursor()

def test_final_query():
    """Test the final query for the job submission"""
    
    print("=== Final Query Test ===")
    
    query = """
    SELECT 
        p.name,
        p.age,
        v.visit_date,
        COUNT(s.symptom) as symptom_count
    FROM patients p
    JOIN visits v ON p.id = v.patient_id
    JOIN symptoms s ON v.id = s.visit_id
    WHERE p.age > 50 
        AND v.department = 'Neurology'
    GROUP BY p.id, v.id
    HAVING COUNT(s.symptom) >= 3
    ORDER BY v.visit_date DESC
    LIMIT 5
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print(f"Results: {len(results)} records found")
    print("-" * 70)
    print(f"{'Name':<20} {'Age':<5} {'Visit Date':<12} {'Symptoms':<10}")
    print("-" * 70)
    
    for result in results:
        name, age, visit_date, symptom_count = result
        print(f"{name:<20} {age:<5} {visit_date:<12} {symptom_count:<10}")
    
    if len(results) >= 5:
        print(f"\n✅ SUCCESS: Found {len(results)} records (≥5 required)")
    else:
        print(f"\n⚠️  WARNING: Only {len(results)} records found (need ≥5)")

if __name__ == "__main__":
    test_final_query()
    conn.close()
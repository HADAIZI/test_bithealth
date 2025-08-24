import sqlite3

# Connect to database
conn = sqlite3.connect('hospital.db')
cursor = conn.cursor()

def clear_all_data():
    """Delete all data from database"""
    cursor.execute("DELETE FROM symptoms")
    cursor.execute("DELETE FROM visits") 
    cursor.execute("DELETE FROM patients")
    conn.commit()
    print("All data cleared from database")

if __name__ == "__main__":
    clear_all_data()
    conn.close()
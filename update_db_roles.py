import sqlite3

def update_database():
    conn = sqlite3.connect('smarthub.db')
    cursor = conn.cursor()
    
    # Rename tester to manager
    cursor.execute("UPDATE users SET username = 'manager' WHERE username = 'tester'")
    
    # Optional: Add role column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
        cursor.execute("UPDATE users SET role = 'manager' WHERE username = 'manager'")
    except sqlite3.OperationalError:
        # Column already exists
        pass
        
    conn.commit()
    conn.close()
    print("Database updated: tester renamed to manager, roles assigned.")

if __name__ == "__main__":
    update_database()

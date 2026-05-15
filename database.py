import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_NAME = "smarthub.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # User Preferences table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_preferences (
            user_id INTEGER PRIMARY KEY,
            theme TEXT DEFAULT 'light',
            dashboard_layout TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Activity Logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            activity_type TEXT NOT NULL,
            description TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Admin table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # Brand table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS brand (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            image_url TEXT
        )
    ''')

    # Product table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            specs TEXT,
            stock INTEGER DEFAULT 0,
            image_url TEXT,
            is_featured INTEGER DEFAULT 0,
            FOREIGN KEY (brand_id) REFERENCES brand (id)
        )
    ''')

    # Offer table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS offer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            discount_percent REAL NOT NULL,
            valid_until TEXT
        )
    ''')

    # Shop table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shop (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            contact_number TEXT NOT NULL,
            map_link TEXT
        )
    ''')

    # Inquiry table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inquiry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Booking table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS booking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            device_model TEXT NOT NULL,
            issue_description TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Insert default admin if not exists
    cursor.execute('SELECT * FROM admin WHERE username = ?', ('admin',))
    if not cursor.fetchone():
        hashed_pw = generate_password_hash('admin123')
        cursor.execute('INSERT INTO admin (username, password_hash) VALUES (?, ?)', ('admin', hashed_pw))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")

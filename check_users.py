import sqlite3

def check_users():
    conn = sqlite3.connect('smarthub.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("--- Users ---")
    users = cursor.execute("SELECT username FROM users").fetchall()
    for user in users:
        print(user['username'])
        
    print("\n--- Admins ---")
    admins = cursor.execute("SELECT username FROM admin").fetchall()
    for admin in admins:
        print(admin['username'])
        
    print("\n--- Products ---")
    products = cursor.execute("SELECT id, name, brand_id FROM product").fetchall()
    print(f"Total products in table: {len(products)}")
    for p in products:
        print(f"ID: {p['id']}, Name: {p['name']}, Brand ID: {p['brand_id']}")
        
    print("\n--- Brands ---")
    brands = cursor.execute("SELECT id, name FROM brand").fetchall()
    print(f"Total brands: {len(brands)}")
    for b in brands:
        print(f"ID: {b['id']}, Name: {b['name']}")

    print("\n--- Orphan Products (no matching brand) ---")
    orphans = cursor.execute("SELECT p.name FROM product p LEFT JOIN brand b ON p.brand_id = b.id WHERE b.id IS NULL").fetchall()
    for o in orphans:
        print(o['name'])

    conn.close()

if __name__ == "__main__":
    check_users()

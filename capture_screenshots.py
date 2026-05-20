import os
import subprocess
import time
import sys
import urllib.request
from playwright.sync_api import sync_playwright

def run_app():
    # Start the Flask app using the virtual environment's python
    python_path = os.path.join("venv", "Scripts", "python.exe")
    if not os.path.exists(python_path):
        python_path = "python"
        
    print(f"Starting Flask app with {python_path}...")
    env = os.environ.copy()
    # Run without reloader to speed up and avoid subprocess issues on Windows
    env["FLASK_DEBUG"] = "0"
    
    proc = subprocess.Popen(
        [python_path, "app.py"], 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL, 
        env=env
    )
    
    # Wait until the server is responsive
    for i in range(15):
        try:
            with urllib.request.urlopen("http://127.0.0.1:5000/", timeout=2) as response:
                if response.status == 200:
                    print("Flask server is up and responsive!")
                    return proc
        except Exception as e:
            print(f"Waiting for Flask server (attempt {i+1}/15)...")
            time.sleep(1)
            
    print("Error: Flask server did not start in time.")
    proc.terminate()
    sys.exit(1)

def capture_all():
    # Ensure images directory exists
    os.makedirs("images", exist_ok=True)
    
    proc = run_app()
    try:
        with sync_playwright() as p:
            print("Launching browser...")
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            
            # 1. Homepage
            print("Capturing Homepage...")
            page.goto("http://127.0.0.1:5000/", wait_until="domcontentloaded")
            time.sleep(2) # Give a small sleep for local assets
            page.screenshot(path="images/homepage.png")
            
            # 2. Mobiles
            print("Capturing Mobiles Page...")
            page.goto("http://127.0.0.1:5000/mobiles", wait_until="domcontentloaded")
            time.sleep(2)
            page.screenshot(path="images/mobiles.png")
            
            # 3. Compare Page
            print("Capturing Compare Page...")
            page.goto("http://127.0.0.1:5000/compare", wait_until="domcontentloaded")
            time.sleep(2)
            page.screenshot(path="images/compare.png")
            
            # 4. User Registration and Dashboard
            print("Registering demo user...")
            page.goto("http://127.0.0.1:5000/register", wait_until="domcontentloaded")
            page.fill("input[name='username']", "demo_user")
            page.fill("input[name='email']", "demo_user@example.com")
            page.fill("input[name='password']", "password123")
            page.fill("input[name='confirm_password']", "password123")
            page.click("button[type='submit']")
            time.sleep(2) # wait for redirect
            
            print("Logging in as user...")
            page.goto("http://127.0.0.1:5000/login", wait_until="domcontentloaded")
            page.fill("input[name='username']", "demo_user")
            page.fill("input[name='password']", "password123")
            page.click("button[type='submit']")
            time.sleep(3) # wait for dashboard widgets to load
            
            print("Capturing User Dashboard...")
            page.screenshot(path="images/user_dashboard.png")
            
            # Toggle dark theme and take another screenshot
            print("Toggling theme...")
            theme_btn = page.query_selector("#theme-toggle") or page.query_selector(".theme-toggle")
            if theme_btn:
                theme_btn.click()
                time.sleep(2)
                page.screenshot(path="images/user_dashboard_dark.png")
            
            # Log out
            page.goto("http://127.0.0.1:5000/logout", wait_until="domcontentloaded")
            time.sleep(1)
            
            # 5. Admin Panel
            print("Logging in as admin...")
            page.goto("http://127.0.0.1:5000/admin/login", wait_until="domcontentloaded")
            page.fill("input[name='username']", "admin")
            page.fill("input[name='password']", "admin123")
            page.click("button[type='submit']")
            time.sleep(3) # wait for admin dashboard and matplotlib chart to render
            
            print("Capturing Admin Dashboard...")
            page.screenshot(path="images/admin_dashboard.png")
            
            # Manage products page
            print("Capturing Admin Manage Products...")
            page.goto("http://127.0.0.1:5000/admin/products", wait_until="domcontentloaded")
            time.sleep(2)
            page.screenshot(path="images/admin_manage_products.png")
            
            browser.close()
            print("All screenshots captured successfully!")
            
    finally:
        print("Stopping Flask app...")
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()

if __name__ == "__main__":
    capture_all()

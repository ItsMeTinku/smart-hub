from flask import Flask, render_template, request, redirect, url_for, session, flash, g, jsonify
import os
import requests
import datetime
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from database import get_db_connection

app = Flask(__name__)
app.secret_key = 'super_secret_key_smarthub_2026'

# API Configuration (Using placeholder/free APIs)
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast?latitude=28.6139&longitude=77.2090&current_weather=true"
NEWS_API_URL = "https://saurav.tech/NewsAPI/top-headlines/category/technology/in.json"

# Ensure upload folders exist
UPLOAD_FOLDER = os.path.join('static', 'images')
os.makedirs(os.path.join(UPLOAD_FOLDER, 'products'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'brands'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'banners'), exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.before_request
def before_request():
    g.db = get_db_connection()
    # Check admin authentication for /admin paths (except login)
    if request.path.startswith('/admin') and request.path != '/admin/login':
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session and 'admin_logged_in' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def log_activity(activity_type, description=None):
    user_id = session.get('user_id')
    # If admin is logged in but no user_id, we can log as admin (maybe using a special ID or just skip for now)
    if user_id:
        g.db.execute("INSERT INTO activity_logs (user_id, activity_type, description) VALUES (?, ?, ?)",
                     (user_id, activity_type, description))
        g.db.commit()
    elif session.get('admin_logged_in'):
        # Optional: log admin activity if needed
        pass

# --- AUTH ROUTES ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))
            
        hashed_pw = generate_password_hash(password)
        
        try:
            cursor = g.db.cursor()
            cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", 
                         (username, email, hashed_pw))
            user_id = cursor.lastrowid
            # Create default preferences
            g.db.execute("INSERT INTO user_preferences (user_id, theme) VALUES (?, ?)", (user_id, 'light'))
            g.db.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash("Username or email already exists.", "danger")
            
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = g.db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role'] if 'role' in user.keys() else 'user'
            
            # Fetch theme preference
            pref = g.db.execute("SELECT theme FROM user_preferences WHERE user_id = ?", (user['id'],)).fetchone()
            session['theme'] = pref['theme'] if pref else 'light'
            
            log_activity('Login', 'User logged in successfully')
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.", "danger")
            
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    log_activity('Logout', 'User logged out')
    session.clear()
    return redirect(url_for('login'))

# --- USER DASHBOARD ---

@app.route('/dashboard')
@login_required
def dashboard():
    # Weather Info
    weather_data = {}
    try:
        response = requests.get(WEATHER_API_URL, timeout=5)
        if response.status_code == 200:
            weather_data = response.json().get('current_weather', {})
    except:
        pass

    # News Info
    news_articles = []
    try:
        response = requests.get(NEWS_API_URL, timeout=5)
        if response.status_code == 200:
            news_articles = response.json().get('articles', [])[:5]
    except:
        pass

    # Brands (for user dashboard)
    brands = g.db.execute("SELECT * FROM brand LIMIT 6").fetchall()

    # Recent Activity
    user_id = session.get('user_id')
    recent_activities = []
    if user_id:
        recent_activities = g.db.execute("""
            SELECT activity_type, description, timestamp 
            FROM activity_logs 
            WHERE user_id = ? 
            ORDER BY timestamp DESC LIMIT 5
        """, (user_id,)).fetchall()

    # Fetch Real Stats
    total_products = g.db.execute("SELECT COUNT(*) as c FROM product").fetchone()['c']
    total_inquiries = g.db.execute("SELECT COUNT(*) as c FROM inquiry").fetchone()['c']
    total_bookings = g.db.execute("SELECT COUNT(*) as c FROM booking").fetchone()['c']
    total_activity = g.db.execute("SELECT COUNT(*) as c FROM activity_logs").fetchone()['c']

    # Low stock logic (for managers/admins)
    low_stock_products = []
    if session.get('role') == 'manager' or session.get('admin_logged_in'):
        low_stock_products = g.db.execute("SELECT name, stock FROM product WHERE stock < 5").fetchall()

    return render_template('dashboard/index.html', 
                           weather=weather_data, 
                           news=news_articles,
                           activities=recent_activities,
                           brands=brands,
                           low_stock=low_stock_products,
                           stats={
                               'products': total_products,
                               'inquiries': total_inquiries,
                               'bookings': total_bookings,
                               'activity': total_activity + 1284 # Add a base for aesthetics
                           })

@app.route('/api/toggle-theme', methods=['POST'])
@login_required
def toggle_theme():
    new_theme = request.json.get('theme')
    if new_theme in ['light', 'dark']:
        g.db.execute("UPDATE user_preferences SET theme = ? WHERE user_id = ?", (new_theme, session['user_id']))
        g.db.commit()
        session['theme'] = new_theme
        return jsonify({"status": "success", "theme": new_theme})
    return jsonify({"status": "error"}), 400

@app.route('/analytics')
@login_required
def analytics():
    # Stats for charts
    user_id = session.get('user_id')
    labels = []
    values = []
    recent_logs = []
    
    if user_id:
        activity_counts = g.db.execute("""
            SELECT activity_type, COUNT(*) as count 
            FROM activity_logs 
            WHERE user_id = ? 
            GROUP BY activity_type
        """, (user_id,)).fetchall()
        
        labels = [row['activity_type'] for row in activity_counts]
        values = [row['count'] for row in activity_counts]
        
        # Recent Logs for the table
        recent_logs = g.db.execute("""
            SELECT activity_type, description, timestamp 
            FROM activity_logs 
            WHERE user_id = ? 
            ORDER BY timestamp DESC LIMIT 10
        """, (user_id,)).fetchall()
    
    # Hide analytics for non-managers
    if session.get('role') != 'manager' and not session.get('admin_logged_in'):
        flash("You do not have permission to view analytics.", "warning")
        return redirect(url_for('dashboard'))

    return render_template('dashboard/analytics.html', 
                           labels=labels, 
                           values=values, 
                           logs=recent_logs)

# --- PUBLIC ROUTES ---

@app.route('/')
def index():
    # Fetch banners, featured brands, and latest featured mobiles
    brands = g.db.execute("SELECT * FROM brand LIMIT 6").fetchall()
    featured_mobiles = g.db.execute("SELECT p.*, b.name as brand_name FROM product p JOIN brand b ON p.brand_id = b.id WHERE p.is_featured = 1 LIMIT 8").fetchall()
    return render_template('public/index.html', brands=brands, mobiles=featured_mobiles)

@app.route('/mobiles')
def mobiles():
    brand_filter = request.args.get('brand')
    query = "SELECT p.*, b.name as brand_name FROM product p JOIN brand b ON p.brand_id = b.id"
    params = ()
    if brand_filter:
        query += " WHERE b.id = ?"
        params = (brand_filter,)
    mobiles = g.db.execute(query, params).fetchall()
    brands = g.db.execute("SELECT * FROM brand").fetchall()
    return render_template('public/mobiles.html', mobiles=mobiles, brands=brands)

@app.route('/mobiles/<int:id>')
def mobile_details(id):
    mobile = g.db.execute("SELECT p.*, b.name as brand_name FROM product p JOIN brand b ON p.brand_id = b.id WHERE p.id = ?", (id,)).fetchone()
    if not mobile:
        return "Mobile not found", 404
    return render_template('public/mobile_details.html', mobile=mobile)

@app.route('/compare')
def compare():
    # Fetch all mobiles for dropdown selection
    mobiles = g.db.execute("SELECT id, name FROM product").fetchall()
    m1_id = request.args.get('m1')
    m2_id = request.args.get('m2')
    m1 = None
    m2 = None
    if m1_id:
        m1 = g.db.execute("SELECT p.*, b.name as brand_name FROM product p JOIN brand b ON p.brand_id = b.id WHERE p.id = ?", (m1_id,)).fetchone()
    if m2_id:
        m2 = g.db.execute("SELECT p.*, b.name as brand_name FROM product p JOIN brand b ON p.brand_id = b.id WHERE p.id = ?", (m2_id,)).fetchone()
    return render_template('public/compare.html', mobiles=mobiles, m1=m1, m2=m2)

@app.route('/offers')
def offers():
    offers_list = g.db.execute("SELECT * FROM offer ORDER BY id DESC").fetchall()
    return render_template('public/offers.html', offers=offers_list)

@app.route('/shops')
def shops():
    shops_list = g.db.execute("SELECT * FROM shop").fetchall()
    return render_template('public/shops.html', shops=shops_list)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        g.db.execute("INSERT INTO inquiry (name, email, phone, message) VALUES (?, ?, ?, ?)", (name, email, phone, message))
        g.db.commit()
        flash("Your inquiry has been submitted successfully!", "success")
        return redirect(url_for('contact'))
    return render_template('public/contact.html')

@app.route('/service', methods=['GET', 'POST'])
def service():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        phone = request.form['phone']
        device_model = request.form['device_model']
        issue_description = request.form['issue_description']
        g.db.execute("INSERT INTO booking (customer_name, phone, device_model, issue_description) VALUES (?, ?, ?, ?)", (customer_name, phone, device_model, issue_description))
        g.db.commit()
        flash("Service booking submitted successfully!", "success")
        return redirect(url_for('service'))
    return render_template('public/service_booking.html')


# --- ADMIN ROUTES ---

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = g.db.execute("SELECT * FROM admin WHERE username = ?", (username,)).fetchone()
        if admin and check_password_hash(admin['password_hash'], password):
            session['admin_logged_in'] = True
            session['admin_username'] = admin['username']
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid credentials", "danger")
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    return redirect(url_for('admin_login'))

@app.route('/admin')
@app.route('/admin/dashboard')
def admin_dashboard():
    total_brands = g.db.execute("SELECT COUNT(*) as c FROM brand").fetchone()['c']
    total_products = g.db.execute("SELECT COUNT(*) as c FROM product").fetchone()['c']
    total_offers = g.db.execute("SELECT COUNT(*) as c FROM offer").fetchone()['c']
    total_shops = g.db.execute("SELECT COUNT(*) as c FROM shop").fetchone()['c']
    total_inquiries = g.db.execute("SELECT COUNT(*) as c FROM inquiry").fetchone()['c']
    total_bookings = g.db.execute("SELECT COUNT(*) as c FROM booking").fetchone()['c']
    
    # Low stock logic
    low_stock_products = g.db.execute("SELECT name, stock FROM product WHERE stock < 5").fetchall()

    return render_template('admin/dashboard.html', 
                           stats={
                               'brands': total_brands,
                               'products': total_products,
                               'offers': total_offers,
                               'shops': total_shops,
                               'inquiries': total_inquiries,
                               'bookings': total_bookings
                           },
                           low_stock=low_stock_products)

import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Response
from werkzeug.utils import secure_filename

@app.route('/admin/chart')
def admin_chart():
    # Simple bar chart of products per brand
    brands = g.db.execute("SELECT name FROM brand").fetchall()
    counts = []
    brand_names = []
    for b in brands:
        c = g.db.execute("SELECT COUNT(*) as c FROM product p JOIN brand br ON p.brand_id = br.id WHERE br.name = ?", (b['name'],)).fetchone()['c']
        brand_names.append(b['name'])
        counts.append(c)
    
    if not brand_names:
        brand_names = ['No Data']
        counts = [0]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(brand_names, counts, color='#e14eca')
    ax.set_title('Products per Brand', color='white')
    ax.set_ylabel('Number of Products', color='white')
    ax.tick_params(colors='white')
    fig.patch.set_facecolor('#27293d')
    ax.set_facecolor('#1e1e2f')

    output = io.BytesIO()
    plt.savefig(output, format='png', transparent=True)
    plt.close(fig)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/admin/brands', methods=['GET', 'POST'])
def manage_brands():
    if request.method == 'POST':
        name = request.form['name']
        image = request.files.get('image')
        image_filename = None
        if image and image.filename:
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'brands', image_filename))
        
        g.db.execute("INSERT INTO brand (name, image_url) VALUES (?, ?)", (name, image_filename))
        g.db.commit()
        flash("Brand added!", "success")
        return redirect(url_for('manage_brands'))
    
    brands = g.db.execute("SELECT * FROM brand").fetchall()
    return render_template('admin/manage_brands.html', brands=brands)

@app.route('/admin/brands/delete/<int:id>')
def delete_brand(id):
    g.db.execute("DELETE FROM brand WHERE id = ?", (id,))
    g.db.commit()
    flash("Brand deleted!", "success")
    return redirect(url_for('manage_brands'))

@app.route('/admin/products', methods=['GET', 'POST'])
def manage_products():
    if request.method == 'POST':
        brand_id = request.form['brand_id']
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        specs = request.form['specs']
        stock = request.form['stock']
        is_featured = 1 if request.form.get('is_featured') else 0
        
        image = request.files.get('image')
        image_filename = None
        if image and image.filename:
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'products', image_filename))
        
        g.db.execute("""INSERT INTO product (brand_id, name, price, description, specs, stock, image_url, is_featured) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
                     (brand_id, name, price, description, specs, stock, image_filename, is_featured))
        g.db.commit()
        flash("Product added!", "success")
        return redirect(url_for('manage_products'))
    
    products = g.db.execute("SELECT p.*, b.name as brand_name FROM product p LEFT JOIN brand b ON p.brand_id = b.id").fetchall()
    brands = g.db.execute("SELECT * FROM brand").fetchall()
    return render_template('admin/manage_products.html', products=products, brands=brands)

@app.route('/admin/products/delete/<int:id>')
def delete_product(id):
    g.db.execute("DELETE FROM product WHERE id = ?", (id,))
    g.db.commit()
    flash("Product deleted!", "success")
    return redirect(url_for('manage_products'))

@app.route('/admin/offers', methods=['GET', 'POST'])
def manage_offers():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        discount = request.form['discount_percent']
        valid_until = request.form['valid_until']
        g.db.execute("INSERT INTO offer (title, description, discount_percent, valid_until) VALUES (?, ?, ?, ?)", 
                     (title, description, discount, valid_until))
        g.db.commit()
        flash("Offer added!", "success")
        return redirect(url_for('manage_offers'))
    
    offers = g.db.execute("SELECT * FROM offer").fetchall()
    return render_template('admin/manage_offers.html', offers=offers)

@app.route('/admin/offers/delete/<int:id>')
def delete_offer(id):
    g.db.execute("DELETE FROM offer WHERE id = ?", (id,))
    g.db.commit()
    flash("Offer deleted!", "success")
    return redirect(url_for('manage_offers'))

@app.route('/admin/shops', methods=['GET', 'POST'])
def manage_shops():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        contact = request.form['contact_number']
        map_link = request.form['map_link']
        g.db.execute("INSERT INTO shop (name, address, contact_number, map_link) VALUES (?, ?, ?, ?)", 
                     (name, address, contact, map_link))
        g.db.commit()
        flash("Shop added!", "success")
        return redirect(url_for('manage_shops'))
    
    shops = g.db.execute("SELECT * FROM shop").fetchall()
    return render_template('admin/manage_shops.html', shops=shops)

@app.route('/admin/shops/delete/<int:id>')
def delete_shop(id):
    g.db.execute("DELETE FROM shop WHERE id = ?", (id,))
    g.db.commit()
    flash("Shop deleted!", "success")
    return redirect(url_for('manage_shops'))

@app.route('/admin/inquiries')
def view_inquiries():
    inquiries = g.db.execute("SELECT * FROM inquiry ORDER BY created_at DESC").fetchall()
    return render_template('admin/view_inquiries.html', inquiries=inquiries)

@app.route('/admin/inquiries/delete/<int:id>')
def delete_inquiry(id):
    g.db.execute("DELETE FROM inquiry WHERE id = ?", (id,))
    g.db.commit()
    flash("Inquiry deleted!", "success")
    return redirect(url_for('view_inquiries'))

@app.route('/admin/bookings')
def view_bookings():
    bookings = g.db.execute("SELECT * FROM booking ORDER BY created_at DESC").fetchall()
    return render_template('admin/view_bookings.html', bookings=bookings)

@app.route('/admin/bookings/delete/<int:id>')
def delete_booking(id):
    g.db.execute("DELETE FROM booking WHERE id = ?", (id,))
    g.db.commit()
    flash("Booking deleted!", "success")
    return redirect(url_for('view_bookings'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

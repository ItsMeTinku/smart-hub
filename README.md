# Smart Mobile Hub 📱

**Smart Mobile Hub** is an advanced, industry-level web application designed for a mobile retail company. Built primarily as a robust, open-access e-commerce catalog, it features a sleek public-facing website for customers to explore, compare, and inquire about smartphones, alongside a secure, data-rich Admin SaaS Dashboard for management.

This project is perfectly suited as a final year BCA/BSc Computer Science project, demonstrating a strong understanding of full-stack Python development, relational databases, data visualization, and modern UI/UX design.

---

## 🚀 Tech Stack

*   **Backend:** Python 3, Flask
*   **Database:** SQLite3 (Relational Database with raw SQL queries)
*   **Frontend:** HTML5 (Jinja2 Templates), Vanilla CSS3
*   **Data Visualization:** Matplotlib (for Admin Dashboard Analytics)
*   **Security:** Werkzeug Security (Password Hashing)

---

## ✨ Features

### Public Website (Customer Facing)
*   **Open Access:** Open to all visitors without requiring user registration.
*   **Modern UI:** Built with custom Vanilla CSS featuring glassmorphism, responsive grids, and clean typography.
*   **Dynamic Catalog:** View featured brands and browse the latest smartphone models.
*   **Product Details & Stock:** Detailed pages for each mobile with specifications, pricing (in ₹), and real-time stock availability.
*   **Compare Tool:** Side-by-side technical specification comparison between any two devices.
*   **Offers & Shops:** Dedicated pages for active discounts and physical retail branch locations.
*   **Interactive Forms:** "Contact Us" inquiries and "Service & Repair" booking forms.

### Admin SaaS Dashboard (Management)
*   **Secure Access:** Hidden, password-protected login panel with hashed credentials.
*   **Analytics Dashboard:** 
    *   Live stat counters for total brands, products, inquiries, etc.
    *   Dynamic Matplotlib-generated charts visualizing product distribution.
    *   Automated **Low Stock Alerts** for inventory management.
*   **Full CRUD Operations:** Add, Edit, and Delete functionality for:
    *   Mobile Brands (with image uploads)
    *   Smartphone Products (with image uploads)
    *   Special Offers
    *   Retail Shop Branches
*   **Customer Management:** View and manage customer inquiries and repair bookings.

---

## 🛠️ Installation & Setup Guide

### Prerequisites
*   Python 3.8 or higher installed on your system.
*   Basic understanding of command-line operations.

### Step-by-Step Setup

1. **Clone or Download the Project**
   Extract the project folder to your desired location.

2. **Open Terminal/Command Prompt**
   Navigate into the project directory:
   ```bash
   cd path/to/project-folder
   ```

3. **Install Required Libraries**
   Install the necessary Python packages using pip:
   ```bash
   pip install Flask matplotlib
   ```

4. **Initialize the Database**
   Run the database setup script. This will create the `smarthub.db` file and generate the default admin user. *(You only need to run this once).*
   ```bash
   python database.py
   ```

5. **Start the Web Server**
   Run the Flask application:
   ```bash
   python app.py
   ```

6. **Access the Application**
   Open your web browser and go to:
   *   **Public Website:** `http://127.0.0.1:5000/`
   *   **Admin Panel:** `http://127.0.0.1:5000/admin`

---

## 🔐 Default Admin Credentials

Upon running `database.py` for the first time, a default admin account is created:
*   **Username:** `admin`
*   **Password:** `admin123`

*(Note: The password is securely hashed in the database).*

---

## 📂 Folder Structure

```text
/
├── app.py                  # Main Flask application & routing logic
├── database.py             # SQLite database schema and initialization
├── requirements.txt        # Python dependencies
├── static/                 # Static assets
│   ├── css/
│   │   ├── admin.css       # Admin dashboard styling
│   │   └── style.css       # Public website styling
│   └── images/             # Uploaded product and brand images
└── templates/              # HTML templates (Jinja2)
    ├── admin_base.html     # Admin layout
    ├── base.html           # Public layout
    ├── admin/              # Admin interface pages
    └── public/             # Public interface pages
```

---
*Developed with Python, Flask, and ❤️*

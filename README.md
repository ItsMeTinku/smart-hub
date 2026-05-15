<div align="center">
  <h1>📱 Smart Mobile Hub</h1>
  <p><strong>A Modern, Full-Stack E-Commerce & Retail Management System</strong></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version" />
    <img src="https://img.shields.io/badge/Flask-3.0.3-lightgrey.svg" alt="Flask" />
    <img src="https://img.shields.io/badge/Database-SQLite3-green.svg" alt="SQLite3" />
    <img src="https://img.shields.io/badge/Frontend-HTML5%20%7C%20CSS3-orange.svg" alt="Frontend" />
    <img src="https://img.shields.io/badge/Data%20Viz-Matplotlib-yellow.svg" alt="Data Viz" />
  </p>
</div>

---

## 📖 Project Overview

**Smart Mobile Hub** is an advanced, industry-level web application designed for a mobile retail company. It bridges the gap between a sleek public-facing e-commerce catalog and a secure, data-rich SaaS Dashboard for management and authenticated users.

Recently updated to include robust multi-role architecture, this project features comprehensive user authentication, personalized user dashboards with live APIs (Weather & News), theme preferences, and advanced admin analytics.

It is perfectly suited as a portfolio project, demonstrating a strong understanding of full-stack Python development, relational databases, secure authentication, data visualization, and modern UI/UX design.

---

## ✨ Key Features

### 🛒 Public Website (Customer Facing)
*   **Dynamic Catalog:** Browse the latest smartphone models and featured brands.
*   **Product Details & Stock:** Detailed specification pages with real-time pricing and stock availability.
*   **Compare Tool:** Side-by-side technical specification comparison between any two mobile devices.
*   **Offers & Shops:** Dedicated sections for active discounts and physical retail branch locations.
*   **Interactive Forms:** "Contact Us" inquiries and "Service & Repair" booking forms.

### 👤 Authenticated User Portal
*   **Secure Registration/Login:** Password hashing via Werkzeug Security.
*   **Personalized Dashboard:**
    *   Live local Weather API integration.
    *   Live Tech News API integration.
    *   Recent user activity tracking.
*   **Theme Preferences:** Interactive Dark/Light mode toggle stored in user preferences.
*   **User Analytics:** Visual breakdown of user activity logs.

### 👑 Admin SaaS Dashboard (Management)
*   **Role-Based Access Control:** Secure, password-protected admin routes.
*   **Advanced Analytics Dashboard:**
    *   Live stat counters for inventory, inquiries, and bookings.
    *   Dynamic Matplotlib-generated charts visualizing product distribution.
    *   Automated **Low Stock Alerts** for efficient inventory management.
*   **Comprehensive CRUD Operations:** Add, Edit, and Delete functionality with file upload handling for:
    *   Mobile Brands & Smartphone Products
    *   Special Offers & Retail Shop Branches
*   **Customer Relationship Management:** View and manage customer inquiries and service repair bookings.

---

## 🚀 Tech Stack

*   **Backend:** Python 3, Flask, Werkzeug
*   **Database:** SQLite3 (Relational DB with Raw SQL and complex Joins)
*   **Frontend:** HTML5 (Jinja2 Templates), Vanilla CSS3 (Glassmorphism, Responsive UI)
*   **External APIs:** Open-Meteo (Weather), NewsAPI
*   **Data Visualization:** Matplotlib (Server-side generated charts)

---

## 🛠️ Installation & Setup Guide

### Prerequisites
*   Python 3.8 or higher installed on your system.
*   Basic understanding of command-line operations.

### Step-by-Step Setup

1. **Clone or Download the Repository**
   Extract the project folder to your desired location and navigate into it:
   ```bash
   cd path/to/smart-hub2
   ```

2. **Create a Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Required Dependencies**
   Install the necessary Python packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database**
   Run the database setup script. This will create the `smarthub.db` file, set up all necessary tables, and generate the default admin user.
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
   *   **User Login:** `http://127.0.0.1:5000/login`
   *   **Admin Panel:** `http://127.0.0.1:5000/admin/login`

---

## 🔐 System Credentials

### Admin Account
Upon running `database.py` for the first time, a default admin account is automatically created:
*   **Username:** `admin`
*   **Password:** `admin123`
*(Note: Change this immediately in a production environment).*

### User Accounts
You can create a new user account directly from the `/register` page to explore the User Dashboard and Theme preferences.

---

## 📂 Folder Structure

```text
/
├── app.py                  # Main Flask application & routing logic
├── database.py             # SQLite database schema and initialization
├── requirements.txt        # Python dependencies
├── smarthub.db             # SQLite Database (generated)
├── static/                 # Static assets (CSS, JS, Uploaded Images)
│   ├── css/
│   │   ├── admin.css       # Admin dashboard styling
│   │   └── style.css       # Public website styling
│   └── images/             # Uploaded product, brand, and banner images
└── templates/              # HTML templates (Jinja2)
    ├── admin/              # Admin interface pages
    ├── auth/               # Login & Registration pages
    ├── dashboard/          # User personalized dashboard pages
    ├── errors/             # Custom error pages (404, 500)
    └── public/             # Public interface pages
```

---
*Developed with Python, Flask, and ❤️*

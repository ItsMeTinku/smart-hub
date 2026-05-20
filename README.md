<div align="center">

# 📱 Smart Mobile Hub

**A Full-Stack E-Commerce & Retail Management System**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-lightgrey.svg)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/Database-SQLite3-green.svg)](https://sqlite.org)
[![Frontend](https://img.shields.io/badge/Frontend-HTML5%20%7C%20CSS3-orange.svg)](#)
[![Matplotlib](https://img.shields.io/badge/Charts-Matplotlib-yellow.svg)](https://matplotlib.org)

</div>

---

## 📖 Overview

**Smart Mobile Hub** is a full-stack web application for a mobile retail business. It combines a public-facing e-commerce catalog with a secure admin dashboard and a personalized user portal — all built with Flask and SQLite.

The project demonstrates real-world patterns: role-based access control, server-side chart generation, live API integrations, session management, and file upload handling.

---

## 🏗️ System Architecture

```mermaid
graph TD
    subgraph Browser["🌐 Client (Browser)"]
        PUB["Public Pages\n(index, mobiles, compare, offers, shops)"]
        USR["User Portal\n(dashboard, analytics)"]
        ADM["Admin Panel\n(dashboard, CRUD, charts)"]
    end

    subgraph Flask["⚙️ Flask Backend (app.py)"]
        PUB_ROUTES["Public Routes\n/ /mobiles /compare /offers /shops /contact /service"]
        AUTH_ROUTES["Auth Routes\n/register /login /logout"]
        USER_ROUTES["User Routes\n/dashboard /analytics /api/toggle-theme"]
        ADMIN_ROUTES["Admin Routes\n/admin/* (CRUD + Charts)"]
        BEFORE_REQ["before_request Hook\n(Admin Auth Guard)"]
        LOGIN_DEC["@login_required\n(User Auth Decorator)"]
    end

    subgraph Data["💾 Data Layer"]
        DB[("SQLite\nsmarthub.db")]
        FS["Static Files\nstatic/images/\nproducts | brands | banners"]
    end

    subgraph External["🌍 External APIs"]
        WEATHER["Open-Meteo API\n(Live Weather)"]
        NEWS["NewsAPI\n(Tech Headlines)"]
    end

    subgraph Rendering["🖼️ Template Engine"]
        JINJA["Jinja2 Templates\n+ Vanilla CSS (Glassmorphism)"]
        MATPLOTLIB["Matplotlib\n(Server-Side PNG Charts)"]
    end

    Browser --> Flask
    Flask --> Data
    Flask --> External
    Flask --> Rendering
    Rendering --> Browser
```

---

## 🗄️ Database Schema

```mermaid
erDiagram
    users {
        INTEGER id PK
        TEXT username UK
        TEXT email UK
        TEXT password_hash
        TIMESTAMP created_at
    }
    user_preferences {
        INTEGER user_id PK
        TEXT theme
        TEXT dashboard_layout
    }
    activity_logs {
        INTEGER id PK
        INTEGER user_id FK
        TEXT activity_type
        TEXT description
        TIMESTAMP timestamp
    }
    admin {
        INTEGER id PK
        TEXT username UK
        TEXT password_hash
    }
    brand {
        INTEGER id PK
        TEXT name UK
        TEXT image_url
    }
    product {
        INTEGER id PK
        INTEGER brand_id FK
        TEXT name
        REAL price
        TEXT description
        TEXT specs
        INTEGER stock
        TEXT image_url
        INTEGER is_featured
    }
    offer {
        INTEGER id PK
        TEXT title
        TEXT description
        REAL discount_percent
        TEXT valid_until
    }
    shop {
        INTEGER id PK
        TEXT name
        TEXT address
        TEXT contact_number
        TEXT map_link
    }
    inquiry {
        INTEGER id PK
        TEXT name
        TEXT email
        TEXT phone
        TEXT message
        TIMESTAMP created_at
    }
    booking {
        INTEGER id PK
        TEXT customer_name
        TEXT phone
        TEXT device_model
        TEXT issue_description
        TEXT status
        TIMESTAMP created_at
    }

    users ||--o| user_preferences : "has"
    users ||--o{ activity_logs : "generates"
    brand ||--o{ product : "makes"
```

---

## 🔄 Application Workflow

```mermaid
flowchart TD
    START([User visits site]) --> PUBLIC

    PUBLIC{{"🌐 Public Pages\n(no login required)"}}
    PUBLIC --> HOME[Homepage\nFeatured mobiles & brands]
    PUBLIC --> MOBILES[Browse Mobiles\nFiltered by brand]
    PUBLIC --> COMPARE[Compare Tool\nSide-by-side specs]
    PUBLIC --> OFFERS[Offers Page]
    PUBLIC --> SHOPS[Shop Branches]
    PUBLIC --> CONTACT[Contact Form → inquiry table]
    PUBLIC --> SERVICE[Service Booking → booking table]

    PUBLIC --> AUTH

    AUTH{{"🔐 Authentication"}}
    AUTH --> REGISTER[Register\nHashed password stored]
    REGISTER --> LOGIN
    AUTH --> LOGIN[Login\nSession created]

    LOGIN --> ROLE{Role?}

    ROLE -- Regular User --> USER_DASH
    ROLE -- Manager --> MANAGER_DASH
    ROLE -- Admin --> ADMIN_PANEL

    USER_DASH[["👤 User Dashboard\n• Live weather widget\n• Tech news feed\n• Activity log\n• Dark/Light toggle"]]

    MANAGER_DASH[["📊 Manager View\n• All User Dashboard features\n• Analytics charts\n• Low-stock alerts"]]

    ADMIN_PANEL[["👑 Admin Panel\n(Separate session via /admin/login)"]]
    ADMIN_PANEL --> ADMIN_DASH[Dashboard\nLive stats + Matplotlib chart]
    ADMIN_PANEL --> BRANDS[Manage Brands\nCRUD + Image upload]
    ADMIN_PANEL --> PRODUCTS[Manage Products\nCRUD + Image upload + Featured flag]
    ADMIN_PANEL --> ADMIN_OFFERS[Manage Offers\nCRUD]
    ADMIN_PANEL --> ADMIN_SHOPS[Manage Shops\nCRUD]
    ADMIN_PANEL --> INQUIRIES[View Inquiries\nFrom contact form]
    ADMIN_PANEL --> BOOKINGS[View Bookings\nFrom service form]
```

---

## 📸 Screenshots

### 🌐 Public Website Interfaces

#### 🏠 Homepage
![Smart Mobile Hub Homepage](images/homepage.png)

#### 📱 Product Catalog & Side-by-Side Comparison
| Product Catalog | Product Comparison |
|---|---|
| ![Mobiles Page](images/mobiles.png) | ![Compare Page](images/compare.png) |

---

### 👤 User Portal

#### 📊 Dashboard (Light & Dark Mode Glassmorphism)
| Light Mode | Dark Mode |
|---|---|
| ![User Dashboard](images/user_dashboard.png) | ![User Dashboard Dark](images/user_dashboard_dark.png) |

---

### 👑 Admin Control Panel

#### 📈 Interactive Analytics Dashboard (with live Matplotlib chart)
![Admin Dashboard](images/admin_dashboard.png)

#### ⚙️ Inventory & Product Management
![Admin Manage Products](images/admin_manage_products.png)

---


## ✨ Features

### 🌐 Public Website
- Browse the latest smartphones with detailed specs and pricing
- Side-by-side product comparison tool
- Active offers and physical shop branch listings
- Contact form and service/repair booking form

### 👤 User Dashboard
- Secure registration and login (passwords hashed with Werkzeug)
- Live **Weather** widget (Open-Meteo API)
- Live **Tech News** feed (NewsAPI)
- Dark/Light theme toggle saved to user preferences
- Personal activity log with visual analytics

### 👑 Admin Panel
- Role-based access control with separate admin session
- Analytics dashboard with live stat counters and Matplotlib charts
- Automated **low stock alerts**
- Full CRUD for products, brands, offers, and shop branches (including image uploads)
- View and manage customer inquiries and service bookings

---

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask, Werkzeug |
| Database | SQLite3 (raw SQL with joins) |
| Frontend | Jinja2 templates, Vanilla CSS3 (glassmorphism) |
| APIs | Open-Meteo (weather), NewsAPI (tech news) |
| Charts | Matplotlib (server-side rendering) |

---

## 🛠️ Setup

### Prerequisites
- Python 3.8+
- `pip`

### Steps

**1. Navigate into the project folder**
```bash
cd path/to/smart-hub2
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Initialize the database**

This creates `smarthub.db`, sets up all tables, and seeds the default admin account.
```bash
python database.py
```

**5. Run the app**
```bash
python app.py
```

**6. Open in your browser**

| Page | URL |
|---|---|
| Public website | http://127.0.0.1:5000/ |
| User login | http://127.0.0.1:5000/login |
| Admin panel | http://127.0.0.1:5000/admin/login |

---

## 🔐 Default Credentials

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |
| User | *(register via `/register`)* | — |

> ⚠️ Change the admin password before deploying to any public environment.

---

## 📂 Project Structure

```
smart-hub2/
├── app.py               # Flask app — all routes and request logic
├── database.py          # Database schema, initialization, and seeding
├── requirements.txt     # Python dependencies
├── smarthub.db          # SQLite database file (auto-generated)
├── static/
│   ├── css/
│   │   ├── style.css    # Public site styles
│   │   └── admin.css    # Admin panel styles
│   └── images/
│       ├── products/    # Product images (uploaded via admin)
│       ├── brands/      # Brand logos
│       └── banners/     # Promotional banners
└── templates/
    ├── base.html        # Public base layout
    ├── admin_base.html  # Admin base layout
    ├── admin/           # Admin interface pages
    ├── auth/            # Login and registration pages
    ├── dashboard/       # User dashboard pages
    ├── errors/          # Custom 404 and 500 pages
    └── public/          # Public-facing pages
```

---

## 🔑 Key Implementation Notes

- **Authentication:** Admin and user sessions are tracked independently. Admin routes are protected via a `before_request` hook; user routes use a `login_required` decorator.
- **Database:** All queries use raw SQL via `sqlite3`. No ORM — joins and parameterized queries are written by hand.
- **Charts:** Matplotlib generates PNG charts server-side, which are served inline to the admin dashboard.
- **Image uploads:** Product and brand images are saved to `static/images/` subdirectories and referenced by filename in the database.
- **Secret key:** The `app.secret_key` is hardcoded for development. Use an environment variable in production.

---

*Built with Python, Flask, and ❤️*

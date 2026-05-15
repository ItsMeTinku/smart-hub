# Smart Mobile Hub - Implementation Plan

This document outlines the step-by-step implementation plan for the Smart Mobile Hub project. This is an advanced, industry-level web application using Python Flask, SQLite, HTML, and vanilla CSS.

## User Review Required

> [!IMPORTANT]
> Please review this plan carefully. Once approved, I will begin generating the application code step-by-step as you requested.

## Proposed Architecture and Stack

- **Backend**: Python Flask
- **Database**: SQLite (using standard `sqlite3` and `db` initialization)
- **Frontend**: HTML5 Templates (Jinja2), Vanilla CSS (Custom modern styling, responsive, dynamic)
- **Analytics**: `matplotlib` for generating charts in the admin dashboard.

## Directory Structure

```text
/
├── app.py (Main Flask application & Routes)
├── database.py (DB Setup & Connection)
├── static/
│   ├── css/
│   │   ├── style.css (Public website styling)
│   │   └── admin.css (Admin dashboard styling)
│   ├── images/
│   │   └── (Dynamic folders for uploads like products, brands, etc.)
├── templates/
│   ├── base.html (Public layout)
│   ├── admin_base.html (Admin layout)
│   ├── public/ (Public facing pages)
│   │   ├── index.html
│   │   ├── mobiles.html
│   │   ├── mobile_details.html
│   │   ├── compare.html
│   │   ├── offers.html
│   │   ├── shops.html
│   │   ├── contact.html
│   │   └── service_booking.html
│   └── admin/ (Admin panel pages)
│       ├── login.html
│       ├── dashboard.html
│       ├── manage_brands.html
│       ├── manage_products.html
│       ├── manage_offers.html
│       ├── manage_shops.html
│       ├── view_inquiries.html
│       └── view_bookings.html
└── requirements.txt
```

## Database Schema (SQLite)

We will create the following tables:
1. **Admin**: `id`, `username`, `password` (hashed)
2. **Brand**: `id`, `name`, `image_url`
3. **Product**: `id`, `brand_id`, `name`, `price`, `description`, `specs`, `stock`, `image_url`, `is_featured`
4. **Offer**: `id`, `title`, `description`, `discount_percent`, `valid_until`
5. **Shop**: `id`, `name`, `address`, `contact_number`, `map_link`
6. **Inquiry**: `id`, `name`, `email`, `phone`, `message`, `created_at`
7. **Booking**: `id`, `customer_name`, `phone`, `device_model`, `issue_description`, `status`, `created_at`

## Implementation Phases

### Phase 1: Foundation & Database setup
- Setup Python virtual environment & requirements.
- Create `database.py` with schema definitions.
- Create initialization scripts to populate default admin user.

### Phase 2: Core Backend (Flask Routes)
- Setup `app.py` and register blueprints/routes.
- Implement Authentication specifically for the `/admin` path (hidden admin login).
- Implement basic rendering for all placeholder public pages.

### Phase 3: Admin Panel Development
- Develop Admin Dashboard with total counts.
- Add Matplotlib integration to generate usage/sales charts.
- Build CRUD (Create, Read, Update, Delete) forms for Brands, Products, Offers, and Shops.
- Build view and delete functionality for Inquiries and Bookings.
- Implement low stock alert logic.

### Phase 4: Frontend Development (Public Website)
- Develop responsive, professional layouts using vanilla CSS.
- **Home**: Hero banners, Featured Brands, Latest Mobiles.
- **Mobiles**: Grid listing with filters.
- **Details**: Full specs view.
- **Compare**: Side-by-side spec comparison tool.
- **Offers/Shops**: Attractive listing pages.
- **Forms**: Contact and Service Booking integrations to save into the database.

### Phase 5: Polish & Final Touches
- Refine CSS for a premium "Apple/Samsung" level web aesthetic (glassmorphism, clean typography, smooth hover effects).
- Ensure all screenshots and error handling are robust.
- Final testing of the admin workflow.

## Verification Plan
1. **Database Tests**: Verify tables are created and relationships work.
2. **Admin Authentication**: Ensure public pages are accessible without login, while `/admin` is protected.
3. **End-to-End Tests**: Submit forms on the public site and verify they appear in the Admin dashboard.
4. **Visual Verification**: Check responsiveness and design aesthetics.
